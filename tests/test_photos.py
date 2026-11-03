import os
from datetime import datetime
from io import BytesIO
from unittest.mock import patch

from PIL import Image

from app.extensions import db
from app.models import ElectricityReading, Photo, Room
from app.services.photos import cleanup_temporary, photo_path, photo_root, process_pending
from app.services.billing import reading_stamp
from test_v1 import AppTestCase


class PhotoTests(AppTestCase):
    def setUp(self):
        super().setUp()
        self.login()

    def submit_meter(self, room, photo=None, **extra):
        data = {"period": "2026-01", f"start_{room.id}": "0", f"end_{room.id}": "10",
                "csrf_token": self.token(), **extra}
        if photo is not None:
            data[f"photo_{room.id}"] = photo
        return self.client.post("/electricity/", data=data)

    def test_new_reading_requires_photo_and_rollback_cleans_staged_files(self):
        one, two = self.room(), self.room("P102")
        result = self.submit_meter(one)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(db.session.query(ElectricityReading).count(), 0)
        result = self.submit_meter(one, self.image_upload(), **{f"start_{two.id}": "0", f"end_{two.id}": "20"})
        self.assertEqual(result.status_code, 400)
        self.assertEqual(db.session.query(ElectricityReading).count(), 0)
        self.assertEqual(db.session.query(Photo).count(), 0)
        self.assertEqual(list((photo_root() / "tmp").iterdir()), [])

    def test_fake_oversized_animated_and_large_pixel_images_are_rejected(self):
        room = self.room()
        for content, name in ((b"not-an-image", "fake.jpg"), (b"<svg/>", "test.svg")):
            self.assertEqual(self.submit_meter(room, (BytesIO(content), name)).status_code, 400)
        with patch.dict(self.app.config, PHOTO_MAX_BYTES=20):
            self.assertEqual(self.submit_meter(room, self.image_upload()).status_code, 400)
        with patch("app.services.photos.MAX_PIXELS", 10):
            self.assertEqual(self.submit_meter(room, self.image_upload()).status_code, 400)
        animation = BytesIO()
        Image.new("RGB", (10, 10), "red").save(animation, "WEBP", save_all=True,
                                              append_images=[Image.new("RGB", (10, 10), "blue")], duration=100)
        animation.seek(0)
        self.assertEqual(self.submit_meter(room, (animation, "animated.webp")).status_code, 400)
        self.assertEqual(db.session.query(Photo).count(), 0)
        self.assertEqual(list((photo_root() / "tmp").iterdir()), [])

    def test_worker_compresses_orients_strips_metadata_and_removes_original(self):
        room = self.room()
        stream = BytesIO()
        exif = Image.Exif()
        exif[274], exif[270] = 6, "private metadata"
        Image.new("RGB", (3000, 1000), "white").save(stream, "JPEG", exif=exif)
        stream.seek(0)
        self.assertEqual(self.submit_meter(room, (stream, "../../private.jpg")).status_code, 302)
        photo = db.session.scalar(db.select(Photo))
        photo_id, source = photo.id, photo_path(photo, True)
        self.assertTrue(source.exists())
        self.assertEqual(self.client.get(f"/photos/{photo_id}").status_code, 404)
        original_size = source.stat().st_size
        self.assertEqual(process_pending(), 1)
        photo = db.session.get(Photo, photo_id)
        self.assertEqual(photo.status, "ready")
        self.assertFalse(source.exists())
        with Image.open(photo_path(photo)) as image:
            self.assertEqual(image.format, "WEBP")
            self.assertEqual(image.size, (733, 2200))
            self.assertFalse(image.getexif())
        self.assertLess(photo_path(photo).stat().st_size, original_size)
        response = self.client.get(f"/photos/{photo_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "image/webp")
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        response.close()
        self.assertEqual(self.app.test_client().get(f"/photos/{photo_id}").status_code, 302)
        self.assertEqual(process_pending(), 0)

    def test_contract_is_optional_and_upload_stays_with_old_tenancy(self):
        room = self.room(status="occupied", tenant_name="Test tenant")
        tenant = room.current_tenancy
        self.assertEqual(tenant.photos, [])
        response = self.post(f"/photos/contract/{tenant.id}", {"photo": self.image_upload()})
        self.assertEqual(response.status_code, 302)
        photo_id = db.session.scalar(db.select(Photo.id))
        tenant.ended_at = datetime.now()
        db.session.commit()
        self.assertEqual(db.session.get(Photo, photo_id).tenancy_id, tenant.id)
        html = self.client.get(f"/rooms/{room.id}").get_data(as_text=True)
        self.assertIn("Test tenant", html)
        self.assertIn("multipart/form-data", html)

    def test_contract_upload_in_room_form_and_invalid_upload_rolls_back_room(self):
        response = self.post("/rooms/new", {"code": "BAD", "status": "vacant", "contract_photos": self.image_upload()})
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(db.session.scalar(db.select(Room).where(Room.code == "BAD")))
        room = self.room(status="occupied", tenant_name="Test tenant")
        tenant = room.current_tenancy
        data = {"code": room.code, "status": "occupied", "tenant_name": tenant.tenant_name,
                "tenancy_id": str(tenant.id), "tenancy_version": str(tenant.version),
                "contract_photos": self.image_upload()}
        for key in ("contract_start", "contract_end", "electricity_price", "water_price", "service_price", "payment_day", "deposit_amount", "rent_price"):
            data[key] = str(getattr(tenant, key))
        self.assertEqual(self.post(f"/rooms/{room.id}/edit", data).status_code, 302)
        self.assertEqual(db.session.query(Photo).count(), 1)
        self.assertEqual(db.session.scalar(db.select(Photo)).tenancy_id, tenant.id)
        fresh = self.room("P103", status="occupied", tenant_name="New tenant", contract_photos=self.image_upload())
        self.assertEqual(len(fresh.current_tenancy.photos), 1)

    def test_correction_requires_new_photo_and_keeps_original_evidence(self):
        room = self.room()
        self.assertEqual(self.submit_meter(room, self.image_upload()).status_code, 302)
        reading = db.session.scalar(db.select(ElectricityReading))
        data = {"action": "confirm", "start_value": "0", "end_value": "20", "reason": "New evidence",
                "stamp": reading_stamp(reading), "csrf_token": self.token()}
        path = f"/electricity/{reading.id}/correct"
        self.assertEqual(self.client.post(path, data=data).status_code, 400)
        self.assertEqual(reading.end_value, 10)
        data["csrf_token"] = self.token()
        self.assertEqual(self.client.post(path, data={**data, "photo": self.image_upload()}).status_code, 302)
        self.assertEqual(reading.end_value, 20)
        self.assertEqual(len(reading.photos), 2)

    def test_worker_failure_reupload_crash_recovery_and_orphan_cleanup(self):
        room = self.room()
        self.assertEqual(self.submit_meter(room, self.image_upload()).status_code, 302)
        photo = db.session.scalar(db.select(Photo))
        photo_id, reading_id = photo.id, photo.reading_id
        source = photo_path(photo, True)
        with self.assertLogs(self.app.logger, level="ERROR"), patch("PIL.Image.Image.save", side_effect=OSError("test failure")):
            self.assertEqual(process_pending(), 1)
        self.assertEqual(db.session.get(Photo, photo_id).status, "failed")
        self.assertFalse(source.exists())
        self.assertEqual(self.post(f"/photos/electricity/{reading_id}", {"photo": self.image_upload()}).status_code, 302)
        replacement = db.session.scalar(db.select(Photo).where(Photo.status == "pending"))
        replacement_id = replacement.id
        # Simulate termination after rename, before updating the DB status.
        Image.new("RGB", (20, 20)).save(photo_path(replacement), "WEBP")
        photo_path(replacement, True).unlink()
        self.assertEqual(process_pending(), 1)
        self.assertEqual(db.session.get(Photo, replacement_id).status, "ready")
        orphan = photo_root() / "tmp" / "orphan.upload"
        orphan.write_bytes(b"orphan")
        os.utime(orphan, (0, 0))
        cleanup_temporary()
        self.assertFalse(orphan.exists())

    def test_upload_auth_csrf_request_limit_and_legacy_readings(self):
        room = self.room()
        reading = ElectricityReading(room_id=room.id, period="2025-01", start_value=0, end_value=1, created_by=self.root_id)
        db.session.add(reading)
        db.session.commit()
        path = f"/photos/electricity/{reading.id}"
        self.assertEqual(self.client.post(path, data={"photo": self.image_upload()}).status_code, 400)
        other = self.app.test_client()
        token = self.token(other, "/login")
        self.assertEqual(other.post(path, data={"csrf_token": token, "photo": self.image_upload()}).status_code, 302)
        self.assertEqual(self.client.get(f"/rooms/{room.id}").status_code, 200)
        token = self.token()
        with patch.dict(self.app.config, MAX_CONTENT_LENGTH=100):
            self.assertEqual(self.client.post(path, data={"csrf_token": token, "photo": self.image_upload()}).status_code, 413)
        self.login("manager", "AdminTest123!")
        self.assertEqual(self.post(path, {"photo": self.image_upload()}).status_code, 302)
        result = self.app.test_cli_runner().invoke(args=["process-photos", "--once"])
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertIn("Processed 1", result.output)

    def test_worker_lock_rejects_second_worker(self):
        lock_path = photo_root() / "worker.lock"
        with lock_path.open("w+b") as lock:
            lock.write(b"0")
            lock.flush()
            lock.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = self.app.test_cli_runner().invoke(args=["process-photos", "--once"])
            self.assertNotEqual(result.exit_code, 0)
            self.assertIn("already running", result.output)
