import re
from io import BytesIO
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from flask import g
from flask.testing import FlaskClient
from sqlalchemy.exc import IntegrityError
from PIL import Image

from app import create_app
from app.extensions import db
from app.models import ElectricityReading, Room, User


class IsolatedRequestClient(FlaskClient):
    def open(self, *args, **kwargs):
        # The suite holds an app context for DB assertions; reset request-local caches.
        for key in ("_login_user", "csrf_token", "csrf_valid"):
            g.pop(key, None)
        return super().open(*args, **kwargs)


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app({
            "TESTING": True, "SECRET_KEY": "test-only-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///" + (Path(self.temp.name) / "test.sqlite3").as_posix(),
            "SESSION_COOKIE_SECURE": False,
            "PHOTO_ROOT": str(Path(self.temp.name) / "uploads"),
        })
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.app.test_client_class = IsolatedRequestClient
        db.create_all()
        root = User(username="root", is_root=True, must_change_password=False)
        root.set_password("RootTest123!")
        admin = User(username="manager", is_root=False, must_change_password=False)
        admin.set_password("AdminTest123!")
        db.session.add_all([root, admin])
        db.session.commit()
        self.root_id, self.admin_id = root.id, admin.id
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.engine.dispose()
        self.ctx.pop()
        self.temp.cleanup()

    def token(self, client=None, page="/"):
        response = (client or self.client).get(page, follow_redirects=True)
        match = re.search(r'name="csrf_token" value="([^"]+)"', response.get_data(as_text=True))
        self.assertIsNotNone(match, response.get_data(as_text=True)[:300])
        return match.group(1)

    def post(self, path, data=None, client=None, page="/", follow=False):
        client = client or self.client
        data = dict(data or {})
        # Existing business tests submit the now-required meter evidence.
        if path == "/electricity/":
            for key, value in list(data.items()):
                if key.startswith("end_") and value:
                    data.setdefault("photo_" + key[4:], self.image_upload())
        if path.startswith("/electricity/") and path.endswith("/correct") and data.get("action") == "confirm":
            data.setdefault("photo", self.image_upload())
        return client.post(path, data={**data, "csrf_token": self.token(client, page)}, follow_redirects=follow)

    def image_upload(self, size=(100, 80)):
        stream = BytesIO()
        Image.new("RGB", size, "white").save(stream, "JPEG")
        stream.seek(0)
        return stream, "test.jpg"

    def login(self, username="root", password="RootTest123!", client=None):
        return self.post("/login", {"username": username, "password": password}, client=client, page="/login")

    def room(self, code="P101", **extra):
        if extra.get("status") == "occupied":
            extra = {"contract_start": "2020-01-01", "contract_end": "2027-01-31", "electricity_price": "4000", "water_price": "100000", "service_price": "150000", "payment_day": "31", "deposit_amount": "0", "rent_price": "3000000", **extra}
        response = self.post("/rooms/new", {"code": code, "status": "vacant", **extra})
        self.assertEqual(response.status_code, 302)
        return db.session.scalar(db.select(Room).where(Room.code == code))


class V1Tests(AppTestCase):
    def test_anonymous_access_and_csrf(self):
        for path in ("/", "/rooms/new", "/electricity/", "/accounts"):
            self.assertEqual(self.client.get(path).status_code, 302)
        self.assertEqual(self.client.post("/login", data={"username": "root"}).status_code, 400)

    def test_root_creates_account_and_first_login_is_gated(self):
        self.login()
        self.assertEqual(self.post("/accounts", {"username": "newadmin", "password": "TempPass123"}).status_code, 302)
        user = db.session.scalar(db.select(User).where(User.username == "newadmin"))
        self.assertTrue(user.must_change_password)
        self.assertNotEqual(user.password_hash, "TempPass123")
        other = self.app.test_client()
        response = self.login("newadmin", "TempPass123", other)
        self.assertIn("/change-password", response.location)
        for path in ("/", "/accounts", "/electricity/", "/rooms/new"):
            self.assertIn("/change-password", other.get(path).location)
        blocked = self.post("/rooms/new", {"code": "BLOCKED", "status": "vacant"}, client=other, page="/change-password")
        self.assertIn("/change-password", blocked.location)
        for password in ("short", "TempPass123"):
            result = self.post("/change-password", {"current_password": "TempPass123", "new_password": password, "confirm_password": password}, client=other, page="/change-password")
            self.assertEqual(result.status_code, 400)
        self.assertEqual(self.post("/change-password", {"current_password": "TempPass123", "new_password": "Eight888", "confirm_password": "Eight888"}, client=other, page="/change-password").status_code, 302)
        self.assertEqual(other.get("/").status_code, 200)
        self.assertFalse(user.must_change_password)

    def test_admin_cannot_manage_accounts_but_can_manage_rooms(self):
        self.login("manager", "AdminTest123!")
        self.assertEqual(self.client.get("/accounts").status_code, 403)
        self.assertEqual(self.post("/accounts", {"username": "illegal", "password": "Password123"}).status_code, 403)
        self.assertEqual(self.post(f"/accounts/{self.root_id}/toggle").status_code, 403)
        self.assertEqual(self.post(f"/accounts/{self.root_id}/reset-password", {"password": "Password123"}).status_code, 403)
        self.room()

    def test_root_cannot_be_disabled_or_reset_by_account_endpoint(self):
        self.login()
        self.assertEqual(self.post(f"/accounts/{self.root_id}/toggle").status_code, 403)
        self.assertEqual(self.post(f"/accounts/{self.root_id}/reset-password", {"password": "Password123"}).status_code, 403)

    def test_reset_and_disable_invalidate_sessions(self):
        self.login()
        other = self.app.test_client()
        self.login("manager", "AdminTest123!", other)
        self.assertEqual(other.get("/").status_code, 200)
        self.post(f"/accounts/{self.admin_id}/reset-password", {"password": "NewTemp123"})
        self.assertEqual(other.get("/").status_code, 302)
        self.assertIn("/change-password", self.login("manager", "NewTemp123", other).location)
        self.post(f"/accounts/{self.admin_id}/toggle")
        self.assertIn("/login", other.get("/").location)
        self.assertEqual(self.login("manager", "NewTemp123", other).status_code, 401)
        self.post(f"/accounts/{self.admin_id}/toggle")
        self.assertIn("/change-password", self.login("manager", "NewTemp123", other).location)

    def test_login_lock_and_duplicate_account(self):
        for _ in range(5):
            self.assertEqual(self.login(password="wrong").status_code, 401)
        self.assertEqual(self.login().status_code, 401)
        root = db.session.get(User, self.root_id)
        root.locked_until = None
        db.session.commit()
        self.login()
        self.assertEqual(self.post("/accounts", {"username": "ROOT", "password": "TempPass123"}).status_code, 400)

    def test_password_change_invalidates_other_sessions(self):
        self.login()
        other = self.app.test_client()
        self.login(client=other)
        self.post("/change-password", {"current_password": "RootTest123!", "new_password": "ChangedPass123", "confirm_password": "ChangedPass123"})
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertIn("/login", other.get("/").location)

    def test_room_history_unique_code_and_escaping(self):
        self.login()
        room = self.room(status="occupied", tenant_name="<script>alert(1)</script>", occupants="A\nB", vehicles="59A-123\n59B-456")
        self.assertEqual(room.current_tenancy.people_count, 3)
        self.assertEqual(len(room.current_tenancy.vehicles), 2)
        self.assertIn("&lt;script&gt;", self.client.get(f"/rooms/{room.id}").get_data(as_text=True))
        self.assertEqual(self.post("/rooms/new", {"code": "p101", "status": "vacant"}).status_code, 400)
        self.post(f"/rooms/{room.id}/edit", {"code": "P101", "status": "occupied", "tenant_name": "New tenant", "new_tenancy": "on", "tenancy_id": str(room.current_tenancy.id), "tenancy_version": str(room.current_tenancy.version), "move_out_date": "2020-02-01", "contract_start": "2020-02-01", "contract_end": "2027-01-31", "electricity_price": "4000", "water_price": "0", "service_price": "0", "payment_day": "1", "deposit_amount": "0", "rent_price": "3000000"})
        db.session.expire_all()
        self.assertEqual(len(room.tenancies), 2)
        self.assertIsNotNone(room.tenancies[0].ended_at)
        self.assertEqual(room.current_tenancy.tenant_name, "New tenant")
        self.post(f"/rooms/{room.id}/remove", {"tenancy_id": str(room.current_tenancy.id), "tenancy_version": str(room.current_tenancy.version), "move_out_date": "2020-03-01"})
        self.assertFalse(room.active)
        self.assertIsNone(room.current_tenancy)
        self.assertEqual(len(room.tenancies), 2)
        empty = self.room("P102")
        empty_id = empty.id
        self.post(f"/rooms/{empty_id}/remove")
        self.assertIsNone(db.session.get(Room, empty_id))

    def test_electricity_chain_partial_save_and_immutable_history(self):
        self.login()
        room = self.room()
        room2 = self.room("P102")
        data = {"period": "2026-01", f"start_{room.id}": "100", f"end_{room.id}": "150"}
        self.assertEqual(self.post("/electricity/", data).status_code, 302)
        self.assertEqual(len(room2.readings), 0)
        self.assertEqual(self.post("/electricity/", data).status_code, 400)
        result = self.post("/electricity/", {"period": "2026-02", f"start_{room.id}": "0", f"end_{room.id}": "180"})
        self.assertEqual(result.status_code, 302)
        db.session.expire_all()
        self.assertEqual(room.readings[1].start_value, 150)
        self.assertEqual(room.readings[1].consumption, 30)
        self.assertEqual(self.post("/electricity/", {"period": "2026-04", f"end_{room.id}": "200"}).status_code, 400)
        self.assertEqual(self.post("/electricity/", {"period": "2025-12", f"start_{room.id}": "0", f"end_{room.id}": "90"}).status_code, 400)
        self.assertEqual(len(room.readings), 2)

    def test_electricity_validation_and_atomic_batch(self):
        self.login()
        one, two = self.room("P101"), self.room("P102")
        for start, end in (("100", "99"), ("", "100"), ("0", "-1"), ("0", "1.2"), ("0", "2147483648")):
            response = self.post("/electricity/", {"period": "2026-01", f"start_{one.id}": "0", f"end_{one.id}": "10", f"start_{two.id}": start, f"end_{two.id}": end})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(db.session.scalar(db.select(db.func.count()).select_from(ElectricityReading)), 0)
        self.assertEqual(self.post("/electricity/", {"period": "2999-01", f"start_{one.id}": "0", f"end_{one.id}": "10"}).status_code, 400)

    def test_db_constraints_and_sqlite_pragmas(self):
        self.login()
        room = self.room()
        self.assertEqual(db.session.execute(db.text("PRAGMA foreign_keys")).scalar(), 1)
        self.assertEqual(db.session.execute(db.text("PRAGMA journal_mode")).scalar(), "wal")
        invalid = ElectricityReading(room_id=room.id, period="2026-01", start_value=100, end_value=50, created_by=self.root_id)
        db.session.add(invalid)
        with self.assertRaises(IntegrityError):
            db.session.commit()
        db.session.rollback()

    def test_all_pages_render_and_headers(self):
        self.login()
        room = self.room()
        for path in ("/", "/?period=bad", f"/rooms/{room.id}", f"/rooms/{room.id}/edit", "/rooms/new", "/electricity/", "/accounts", "/change-password"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)
            self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertEqual(self.client.get("/rooms/9999").status_code, 404)

    def test_backup_is_consistent_and_never_overwrites(self):
        target = Path(self.temp.name) / "backup.sqlite3"
        runner = self.app.test_cli_runner()
        self.assertEqual(runner.invoke(args=["backup-db", str(target)]).exit_code, 0)
        with closing(sqlite3.connect(target)) as connection:
            self.assertEqual(connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertEqual(connection.execute("SELECT count(*) FROM user").fetchone()[0], 2)
        self.assertNotEqual(runner.invoke(args=["backup-db", str(target)]).exit_code, 0)

    def test_initial_admin_command_does_not_reset_existing_user(self):
        old_hash = db.session.get(User, self.root_id).password_hash
        result = self.app.test_cli_runner().invoke(args=["init-admin"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(db.session.get(User, self.root_id).password_hash, old_hash)

    def test_initial_admin_bootstrap_requires_password_change(self):
        db.drop_all()
        db.create_all()
        with patch.dict("os.environ", {"INITIAL_ADMIN_USERNAME": "root", "INITIAL_ADMIN_PASSWORD": "InitialTest123"}):
            result = self.app.test_cli_runner().invoke(args=["init-admin"])
        self.assertEqual(result.exit_code, 0, result.output)
        user = db.session.scalar(db.select(User).where(User.username == "root"))
        self.assertTrue(user.is_root)
        self.assertTrue(user.must_change_password)
        self.assertTrue(user.check_password("InitialTest123"))
        self.assertIn("/change-password", self.login("root", "InitialTest123").location)

    def test_migrations_build_a_fresh_database(self):
        migrated = create_app({
            "TESTING": True, "SECRET_KEY": "migration-only-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///" + (Path(self.temp.name) / "migrated.sqlite3").as_posix(),
        })
        with migrated.app_context():
            result = migrated.test_cli_runner().invoke(args=["db", "upgrade"])
            self.assertEqual(result.exit_code, 0, f"{result.output}\n{result.exception}")
            self.assertEqual(db.session.scalar(db.select(db.func.count()).select_from(Room)), 0)
            self.assertEqual(db.session.execute(db.text("SELECT version_num FROM alembic_version")).scalar(), "f13a98c52b70")
            db.session.remove()
            db.engine.dispose()

    def test_boosted_expired_session_redirects_without_partial_login(self):
        response = self.client.get("/", headers={"HX-Request": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("/login", response.headers["HX-Redirect"])


if __name__ == "__main__":
    unittest.main()
