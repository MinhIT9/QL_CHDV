import os
from datetime import datetime
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from PIL import Image
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app import create_app
from app.models import ElectricityReading, MonthlyBill, Photo, Room
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

    def test_new_reading_allows_no_photo_and_invalid_photo_rolls_back_batch(self):
        one, two = self.room(), self.room("P102")
        result = self.submit_meter(one)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(db.session.query(ElectricityReading).count(), 1)
        result = self.submit_meter(one, self.image_upload(), period="2026-02", **{f"start_{two.id}": "0", f"end_{two.id}": "20", f"photo_{two.id}": (BytesIO(b"fake"), "fake.jpg")})
        self.assertEqual(result.status_code, 400)
        self.assertEqual(db.session.query(ElectricityReading).count(), 1)
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

    def test_correction_allows_no_photo_and_keeps_original_evidence(self):
        room = self.room()
        self.assertEqual(self.submit_meter(room, self.image_upload()).status_code, 302)
        reading = db.session.scalar(db.select(ElectricityReading))
        data = {"action": "confirm", "start_value": "0", "end_value": "20", "reason": "New evidence",
                "stamp": reading_stamp(reading), "csrf_token": self.token()}
        path = f"/electricity/{reading.id}/correct"
        self.assertEqual(self.client.post(path, data=data).status_code, 302)
        self.assertEqual(reading.end_value, 20)
        self.assertEqual(len(reading.photos), 1)
        process_pending()
        reading = db.session.get(ElectricityReading, reading.id)
        data.update(end_value="30", stamp=reading_stamp(reading))
        data["csrf_token"] = self.token()
        self.assertEqual(self.client.post(path, data={**data, "photo": self.image_upload()}).status_code, 302)
        self.assertEqual(reading.end_value, 30)
        self.assertEqual(len(reading.photos), 1)

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

    def test_ajax_meter_save_without_photo_and_validation_preserve_other_rows(self):
        one, two = self.room(), self.room("P102")
        response = self.client.post('/electricity/', data={"period": "2026-01", f"start_{one.id}": "0", f"end_{one.id}": "10", "csrf_token": self.token()}, headers={"X-Meter-Save": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertIn('data-room-id=', response.json['html'])
        self.assertEqual(db.session.query(ElectricityReading).count(), 1)
        response = self.client.post('/electricity/', data={"period": "2026-01", f"start_{two.id}": "10", f"end_{two.id}": "0", "csrf_token": self.token()}, headers={"X-Meter-Save": "1"})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(db.session.query(ElectricityReading).count(), 1)

    def test_ajax_photo_retry_is_idempotent_and_status_is_private(self):
        room = self.room()
        self.assertEqual(self.submit_meter(room).status_code, 302)
        reading = db.session.scalar(db.select(ElectricityReading))
        path = f'/photos/electricity/{reading.id}'
        token = 'a' * 32
        for _ in range(2):
            response = self.client.post(path, data={"photo": self.image_upload(), "upload_token": token, "csrf_token": self.token()}, headers={"X-Photo-Upload": "1"})
            self.assertEqual(response.status_code, 200, response.get_data(as_text=True))
            self.assertEqual(response.json['photo']['status'], 'pending')
        self.assertEqual(db.session.query(Photo).count(), 1)
        photo_id = response.json['photo']['id']
        self.assertEqual(self.app.test_client().get(f'/photos/status?ids={photo_id}').status_code, 302)
        response = self.client.get(f'/photos/status?ids={photo_id}')
        self.assertIsNone(response.json['photos'][0]['url'])
        process_pending()
        response = self.client.get(f'/photos/status?ids={photo_id}')
        self.assertEqual(response.json['photos'][0]['status'], 'ready')
        self.assertTrue(response.json['photos'][0]['url'].startswith(f'/photos/{photo_id}?v='))
        self.assertEqual(self.client.get('/photos/status?ids=bad').status_code, 400)
        self.assertEqual(self.client.get('/photos/status?ids=' + ','.join(['1'] * 101)).status_code, 400)
        self.assertEqual(self.client.get('/photos/status?ids=' + '1' * 1000).status_code, 400)

    def test_ajax_invalid_photo_cleans_temp_and_token_cannot_cross_owner(self):
        room = self.room()
        self.submit_meter(room)
        reading = db.session.scalar(db.select(ElectricityReading))
        path = f'/photos/electricity/{reading.id}'
        response = self.client.post(path, data={"photo": (BytesIO(b'bad'), 'bad.jpg'), "upload_token": 'b' * 32, "csrf_token": self.token()}, headers={"X-Photo-Upload": "1"})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(list((photo_root() / 'tmp').iterdir()), [])
        token = 'c' * 32
        response = self.client.post(path, data={"photo": self.image_upload(), "upload_token": token, "csrf_token": self.token()}, headers={"X-Photo-Upload": "1"})
        self.assertEqual(response.status_code, 200)
        other_room = self.room('P102')
        self.submit_meter(other_room)
        other_reading = db.session.scalar(db.select(ElectricityReading).where(ElectricityReading.room_id == other_room.id))
        response = self.client.post(f'/photos/electricity/{other_reading.id}', data={"photo": self.image_upload(), "upload_token": token, "csrf_token": self.token()}, headers={"X-Photo-Upload": "1"})
        self.assertEqual(response.status_code, 409)
        self.assertEqual(db.session.query(Photo).count(), 1)

    def test_replacement_keeps_one_record_preserves_old_on_failure_then_deletes_it(self):
        room = self.room()
        self.submit_meter(room, self.image_upload())
        process_pending()
        photo = db.session.scalar(db.select(Photo))
        photo_id, reading_id, old_path = photo.id, photo.reading_id, photo_path(photo)
        path = f'/photos/electricity/{reading_id}'
        # Invalid input does not change the old record/file.
        self.post(path, {'photo': (BytesIO(b'bad'), 'bad.jpg')})
        self.assertEqual(db.session.get(Photo, photo_id).status, 'ready')
        self.assertTrue(old_path.exists())
        self.post(path, {'photo': self.image_upload()})
        photo = db.session.get(Photo, photo_id)
        self.assertEqual(db.session.query(Photo).count(), 1)
        self.assertTrue(old_path.exists())
        response = self.client.get(f'/photos/{photo_id}')
        self.assertEqual(response.status_code, 200)
        response.close()
        # A second replacement is rejected while compression is pending.
        response = self.client.post(path, data={'photo': self.image_upload(), 'upload_token': 'd' * 32, 'csrf_token': self.token()}, headers={'X-Photo-Upload': '1'})
        self.assertEqual(response.status_code, 400)
        with self.assertLogs(self.app.logger, level='ERROR'), patch('PIL.Image.Image.save', side_effect=OSError('test failure')):
            process_pending()
        photo = db.session.get(Photo, photo_id)
        self.assertEqual(photo.status, 'failed')
        self.assertIsNotNone(photo.previous_token)
        self.assertTrue(old_path.exists())
        self.post(path, {'photo': self.image_upload()})
        process_pending()
        photo = db.session.get(Photo, photo_id)
        self.assertEqual(photo.status, 'ready')
        self.assertIsNone(photo.previous_token)
        self.assertFalse(old_path.exists())
        self.assertTrue(photo_path(photo).exists())
        self.assertEqual(db.session.query(Photo).count(), 1)

    def test_active_bill_freezes_photo_for_root_and_admin_and_pending_blocks_billing(self):
        room = self.room(status='occupied', tenant_name='Test tenant')
        self.submit_meter(room, self.image_upload())
        reading = db.session.scalar(db.select(ElectricityReading))
        reading_id = reading.id
        tenant = room.current_tenancy
        bill_data = {'action': 'confirm', 'period': reading.period, 'tenancy_id': str(tenant.id), 'tenancy_version': str(tenant.version),
                     'stamp': reading_stamp(reading), 'rent_price': '3000000', 'water_price': '100000', 'service_price': '150000',
                     'electricity_price': '4000', 'people_count': '1', 'payment_day': '31'}
        self.assertEqual(self.post(f'/rooms/{room.id}/bill', bill_data).status_code, 400)
        process_pending()
        self.assertEqual(self.post(f'/rooms/{room.id}/bill', bill_data).status_code, 302)
        photo = db.session.scalar(db.select(Photo))
        token, photo_id = photo.token, photo.id
        for username, password in (('root', 'RootTest123!'), ('manager', 'AdminTest123!')):
            self.login(username, password)
            response = self.client.post(f'/photos/electricity/{reading_id}', data={'photo': self.image_upload(), 'upload_token': 'e' * 32, 'csrf_token': self.token()}, headers={'X-Photo-Upload': '1'})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(db.session.get(Photo, photo_id).token, token)
        html = self.client.get('/electricity/?period=2026-01').get_data(as_text=True)
        self.assertNotIn('name="photo_' + str(room.id) + '"', html)
        self.assertIn('meter-photo-widget', html)
        # Cancelling the effective bill unlocks the image; an ordinary receipt is not required to freeze it.
        bill = db.session.scalar(db.select(MonthlyBill))
        bill.cancelled_at = datetime.now()
        db.session.commit()
        response = self.client.post(f'/photos/electricity/{reading_id}', data={'photo': self.image_upload(), 'upload_token': 'f' * 32, 'csrf_token': self.token()}, headers={'X-Photo-Upload': '1'})
        self.assertEqual(response.status_code, 200)

    def test_migration_reduces_legacy_duplicates_and_database_enforces_single_photo(self):
        app = create_app({'TESTING': True, 'SECRET_KEY': 'migration-test-only',
                          'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + (Path(self.temp.name) / 'old-photos.sqlite3').as_posix()})
        with app.app_context():
            try:
                result = app.test_cli_runner().invoke(args=['db', 'upgrade', 'f13a98c52b70'])
                self.assertEqual(result.exit_code, 0, result.output)
                from app.models import User
                user = User(username='test', password_hash='unused-test-hash')
                room = Room(code='OLD')
                db.session.add_all([user, room])
                db.session.flush()
                reading = ElectricityReading(room_id=room.id, period='2026-01', start_value=0, end_value=1, created_by=user.id)
                db.session.add(reading)
                db.session.flush()
                for index, state in enumerate(('ready', 'ready', 'pending')):
                    db.session.execute(db.text('INSERT INTO photo (token,reading_id,status,created_by,created_at) VALUES (:token,:reading,:status,:user,:created)'),
                                       {'token': str(index) * 32, 'reading': reading.id, 'status': state, 'user': user.id, 'created': datetime.now()})
                db.session.commit()
                result = app.test_cli_runner().invoke(args=['db', 'upgrade'])
                self.assertEqual(result.exit_code, 0, result.output)
                photos = db.session.scalars(db.select(Photo)).all()
                self.assertEqual(len(photos), 1)
                self.assertEqual(photos[0].token, '1' * 32)
                with self.assertRaises(IntegrityError):
                    db.session.execute(db.text('INSERT INTO photo (token,reading_id,status,created_by,created_at) VALUES (:token,:reading,:status,:user,:created)'),
                                       {'token': 'x' * 32, 'reading': reading.id, 'status': 'ready', 'user': user.id, 'created': datetime.now()})
                db.session.rollback()
            finally:
                db.session.remove()
                db.engine.dispose()

    def test_meter_photo_upload_is_available_on_electricity_page_without_changing_reading(self):
        room = self.room()
        reading = ElectricityReading(room_id=room.id, period="2026-01", start_value=10, end_value=20, created_by=self.root_id)
        db.session.add(reading)
        db.session.commit()
        path = f"/electricity/{reading.id}/correct"
        html = self.client.get(path).get_data(as_text=True)
        upload_path = f"/photos/electricity/{reading.id}"
        self.assertIn('id="meter-photos"', html)
        self.assertIn(f'data-upload-url="{upload_path}"', html)
        self.assertIn('type="file"', html)
        response = self.post(upload_path, {"photo": self.image_upload()})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith(path + "#meter-photos"))
        self.assertEqual((reading.start_value, reading.end_value), (10, 20))
        self.assertEqual(len(reading.photos), 1)
        html = self.client.get('/electricity/?period=2026-01').get_data(as_text=True)
        self.assertIn(f'data-upload-url="{upload_path}"', html)
        room_html = self.client.get(f'/rooms/{room.id}').get_data(as_text=True)
        self.assertNotIn(f'action="{upload_path}"', room_html)
