from datetime import date
from pathlib import Path
from unittest.mock import patch

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import StaleDataError

from app import create_app
from app.extensions import db
from app.models import ContractRenewal, Room, Tenancy
from app.services.contracts import add_months, due_date
from test_v1 import AppTestCase


class ContractTests(AppTestCase):
    def setUp(self):
        super().setUp()
        fixed_today = patch("app.services.contracts.local_today", return_value=date(2026, 11, 2))
        fixed_today.start()
        self.addCleanup(fixed_today.stop)
        self.login()

    def edit_data(self, room, **extra):
        tenant = room.current_tenancy
        data = {"code": room.code, "status": "occupied", "tenant_name": tenant.tenant_name,
                "tenancy_id": str(tenant.id), "tenancy_version": str(tenant.version)}
        for key in ("contract_start", "contract_end", "water_price", "service_price", "rent_price", "deposit_amount", "payment_day"):
            value = getattr(tenant, key)
            data[key] = value.isoformat() if hasattr(value, "isoformat") else str(value) if value is not None else ""
        return {**data, **extra}

    def renewal_data(self, room, **extra):
        tenant = room.current_tenancy
        return {"tenancy_id": str(tenant.id), "tenancy_version": str(tenant.version), "months": "1", "action": "preview", **extra}

    def test_zero_prices_are_saved_and_distinct_from_unknown(self):
        room = self.room(status="occupied", tenant_name="Example", water_price="0", service_price="0")
        self.assertEqual(room.current_tenancy.monthly_fees, 0)
        self.assertIn("0 đ", self.client.get(f"/rooms/{room.id}").get_data(as_text=True))
        legacy = Room(code="OLD", active=True)
        legacy.tenancies.append(Tenancy(tenant_name="Legacy"))
        db.session.add(legacy)
        db.session.commit()
        self.assertIsNone(legacy.current_tenancy.monthly_fees)
        page = self.client.get(f"/rooms/{legacy.id}").get_data(as_text=True)
        self.assertIn("Chưa cập nhật", page)
        self.assertEqual(self.post(f"/rooms/{legacy.id}/edit", self.edit_data(legacy, note="Legacy edit")).status_code, 302)
        self.assertIsNone(legacy.current_tenancy.water_price)

    def test_new_tenancy_requires_terms_and_valid_amounts(self):
        base = {"code": "NEW", "status": "occupied", "tenant_name": "Example", "contract_start": "2020-01-01", "contract_end": "2027-01-31", "payment_day": "31", "deposit_amount": "0", "rent_price": "3000000", "water_price": "0", "service_price": "0"}
        for field in ("water_price", "service_price", "rent_price", "deposit_amount", "payment_day", "contract_start", "contract_end"):
            self.assertEqual(self.post("/rooms/new", {**base, field: ""}).status_code, 400, field)
        for field, values in (("water_price", ("-1", "1.5", "100k", "2147483648")), ("service_price", ("-1", "1.5")), ("payment_day", ("0", "32", "1.5")), ("contract_start", ("2020-02-30", "2999-01-01")), ("contract_end", ("2019-12-31",))):
            for value in values:
                self.assertEqual(self.post("/rooms/new", {**base, field: value}).status_code, 400, (field, value))
        self.assertEqual(db.session.scalar(db.select(db.func.count()).select_from(Room)), 0)

    def test_fee_estimate_and_due_dates(self):
        room = self.room(status="occupied", tenant_name="Example", occupants="Other")
        tenant = room.current_tenancy
        self.assertEqual(tenant.monthly_fees, 350000)
        self.assertEqual(tenant.monthly_total, 3350000)
        self.assertEqual(due_date(tenant, "2027-02"), date(2027, 2, 28))
        self.assertEqual(due_date(tenant, "2028-02"), date(2028, 2, 29))
        self.assertEqual(due_date(tenant, "2027-03"), date(2027, 3, 31))
        self.assertEqual(tenant.payment_day, 31)

    def test_rent_validation_zero_and_legacy_unknown(self):
        room = self.room(status="occupied", tenant_name="Example", rent_price="4500000")
        tenant = room.current_tenancy
        self.assertEqual(tenant.rent_price, 4500000)
        self.assertIn("4.500.000 đ", self.client.get("/").get_data(as_text=True))
        self.assertIn("<th>Tiền phòng", self.client.get("/").get_data(as_text=True))
        for value in ("", "-1", "1.5", "3000k", "2147483648"):
            self.assertEqual(self.post(f"/rooms/{room.id}/edit", self.edit_data(room, rent_price=value)).status_code, 400)
        self.assertEqual(self.post(f"/rooms/{room.id}/edit", self.edit_data(room, rent_price="0")).status_code, 302)
        self.assertEqual(tenant.rent_price, 0)
        self.assertEqual(tenant.monthly_total, tenant.monthly_fees)
        self.assertIsNone(Tenancy(tenant_name="Legacy").monthly_total)

    def test_unified_start_and_deposit(self):
        room = self.room(status="occupied", tenant_name="Example", deposit_amount="2500000")
        tenant = room.current_tenancy
        self.assertEqual(tenant.deposit_amount, 2500000)
        self.assertEqual(tenant.move_in_date, tenant.contract_start)
        self.assertEqual(tenant.monthly_fees, 250000)
        page = self.client.get(f"/rooms/{room.id}/edit").get_data(as_text=True)
        self.assertNotIn('name="move_in_date"', page)
        self.assertEqual(page.count('name="contract_start"'), 1)
        self.assertIn("2.500.000 đ", self.client.get("/").get_data(as_text=True))
        for value in ("-1", "1.5", "2147483648"):
            self.assertEqual(self.post(f"/rooms/{room.id}/edit", self.edit_data(room, deposit_amount=value)).status_code, 400)
        self.assertEqual(self.post(f"/rooms/{room.id}/edit", self.edit_data(room, deposit_amount="0")).status_code, 302)
        self.assertEqual(tenant.deposit_amount, 0)

    def test_calendar_anchor_and_leap_year(self):
        self.assertEqual(add_months(date(2027, 1, 31), 1, 31), date(2027, 2, 28))
        self.assertEqual(add_months(date(2027, 2, 28), 1, 31), date(2027, 3, 31))
        self.assertEqual(add_months(date(2028, 1, 31), 1, 31), date(2028, 2, 29))
        with self.assertRaises(ValueError):
            add_months(date(9999, 12, 31), 1, 31)

    def test_renewal_preview_confirm_history_and_replay_protection(self):
        room = self.room(status="occupied", tenant_name="Example")
        tenant = room.current_tenancy
        first_id = tenant.id
        payload = self.renewal_data(room)
        response = self.post(f"/rooms/{room.id}/renew", payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(tenant.contract_end, date(2027, 1, 31))
        self.assertEqual(len(tenant.renewals), 0)
        confirm = {**payload, "action": "confirm", "expected_new_end": "2027-02-28"}
        self.assertEqual(self.post(f"/rooms/{room.id}/renew", confirm).status_code, 302)
        db.session.expire_all()
        self.assertEqual(tenant.contract_end, date(2027, 2, 28))
        self.assertEqual(tenant.id, first_id)
        self.assertEqual(len(tenant.renewals), 1)
        self.assertEqual(tenant.renewals[0].created_by, self.root_id)
        self.assertEqual(self.post(f"/rooms/{room.id}/renew", confirm).status_code, 400)
        second = self.renewal_data(room, action="confirm", expected_new_end="2027-03-31")
        self.assertEqual(self.post(f"/rooms/{room.id}/renew", second).status_code, 302)
        db.session.expire_all()
        self.assertEqual(tenant.contract_end, date(2027, 3, 31))
        self.assertEqual(len(tenant.renewals), 2)
        self.assertEqual(self.post(f"/rooms/{room.id}/edit", self.edit_data(room, contract_end="2028-01-31")).status_code, 400)

    def test_expired_renewal_needs_explicit_confirmation(self):
        room = self.room(status="occupied", tenant_name="Example", contract_end="2020-01-31")
        self.assertEqual(room.status, "Đang thuê")
        data = self.renewal_data(room, action="confirm", expected_new_end="2020-02-29")
        self.assertEqual(self.post(f"/rooms/{room.id}/renew", data).status_code, 400)
        self.assertEqual(self.post(f"/rooms/{room.id}/renew", {**data, "confirm_overdue": "on"}).status_code, 302)

    def test_renewal_invalid_inputs_and_unknown_dates(self):
        room = self.room(status="occupied", tenant_name="Example")
        for months in ("", "0", "-1", "1.5", "121"):
            self.assertEqual(self.post(f"/rooms/{room.id}/renew", self.renewal_data(room, months=months)).status_code, 400)
        self.assertEqual(self.post(f"/rooms/{room.id}/renew", self.renewal_data(room, action="confirm")).status_code, 400)
        self.assertEqual(self.post(f"/rooms/{room.id}/renew", self.renewal_data(room, tenancy_id="999")).status_code, 400)
        room.current_tenancy.contract_end = None
        db.session.commit()
        self.assertEqual(self.post(f"/rooms/{room.id}/renew", self.renewal_data(room)).status_code, 400)

    def test_moveout_dates_and_new_tenant_keep_old_terms(self):
        room = self.room(status="occupied", tenant_name="Old")
        old = room.current_tenancy
        data = self.edit_data(room, new_tenancy="on", tenant_name="New", contract_start="2020-03-01", water_price="0", service_price="0")
        for value in ("", "2019-12-31", "2999-01-01"):
            self.assertEqual(self.post(f"/rooms/{room.id}/edit", {**data, "move_out_date": value}).status_code, 400)
        self.assertEqual(self.post(f"/rooms/{room.id}/edit", {**data, "move_out_date": "2020-03-02"}).status_code, 400)
        self.assertEqual(self.post(f"/rooms/{room.id}/edit", {**data, "move_out_date": "2020-03-01"}).status_code, 302)
        db.session.expire_all()
        self.assertEqual(old.water_price, 100000)
        self.assertEqual(old.move_out_date, date(2020, 3, 1))
        self.assertEqual(room.current_tenancy.water_price, 0)
        self.assertNotEqual(old.id, room.current_tenancy.id)

    def test_remove_requires_date_and_stale_edits_are_rejected(self):
        room = self.room(status="occupied", tenant_name="Example")
        payload = self.edit_data(room)
        self.assertEqual(self.post(f"/rooms/{room.id}/remove", payload).status_code, 400)
        self.assertTrue(room.active)
        self.assertEqual(self.post(f"/rooms/{room.id}/edit", {**payload, "water_price": "0"}).status_code, 302)
        self.assertEqual(self.post(f"/rooms/{room.id}/edit", payload).status_code, 400)
        payload = self.edit_data(room, move_out_date="2020-04-01")
        self.assertEqual(self.post(f"/rooms/{room.id}/remove", payload).status_code, 302)
        self.assertIsNone(room.current_tenancy)
        self.assertEqual(self.client.get(f"/rooms/{room.id}/renew").status_code, 302)

    def test_optimistic_lock_rejects_concurrent_database_writes(self):
        room = self.room(status="occupied", tenant_name="Example")
        tenant_id = room.current_tenancy.id
        with Session(db.engine) as one, Session(db.engine) as two:
            first, stale = one.get(Tenancy, tenant_id), two.get(Tenancy, tenant_id)
            first.contract_end = date(2027, 2, 28)
            one.commit()
            stale.contract_end = date(2027, 3, 31)
            with self.assertRaises(StaleDataError):
                two.commit()

    def test_contract_pages_and_payment_status_labels(self):
        room = self.room(status="occupied", tenant_name="Example")
        for path in ("/", f"/rooms/{room.id}", f"/rooms/{room.id}/edit", f"/rooms/{room.id}/renew", f"/rooms/{room.id}/remove"):
            self.assertEqual(self.client.get(path).status_code, 200, path)
        self.assertIn("chưa xác nhận thu", self.client.get("/").get_data(as_text=True))

    def test_upgrade_preserves_legacy_tenant_children_and_checks(self):
        migrated = create_app({"TESTING": True, "SECRET_KEY": "migration-contract-test", "SQLALCHEMY_DATABASE_URI": "sqlite:///" + (Path(self.temp.name) / "legacy.sqlite3").as_posix()})
        with migrated.app_context():
            runner = migrated.test_cli_runner()
            self.assertEqual(runner.invoke(args=["db", "upgrade", "e9329a770fe9"]).exit_code, 0)
            db.session.execute(db.text("INSERT INTO room (id,code,active,note) VALUES (1,'OLD',1,'')"))
            db.session.execute(db.text("INSERT INTO tenancy (id,room_id,tenant_name,started_at) VALUES (1,1,'Legacy','2020-01-01 00:00:00')"))
            db.session.execute(db.text("INSERT INTO occupant (tenancy_id,name) VALUES (1,'Other')"))
            db.session.execute(db.text("INSERT INTO vehicle (tenancy_id,plate) VALUES (1,'TEST')"))
            db.session.commit()
            intermediate = runner.invoke(args=["db", "upgrade", "dd7493777e83"])
            self.assertEqual(intermediate.exit_code, 0, intermediate.output)
            db.session.execute(db.text("UPDATE tenancy SET move_in_date='2020-01-15', contract_end='2027-01-31' WHERE id=1"))
            db.session.execute(db.text("INSERT INTO room (id,code,active,note) VALUES (2,'OTHER',1,''),(3,'CONFLICT',1,'')"))
            db.session.execute(db.text("INSERT INTO tenancy (id,room_id,tenant_name,started_at,move_in_date,contract_start,contract_end) VALUES (2,2,'Other','2020-01-01','2020-01-15','2020-01-01','2027-01-31'),(3,3,'Conflict','2020-01-01','2020-02-01',NULL,'2020-01-31')"))
            db.session.commit()
            result = runner.invoke(args=["db", "upgrade"])
            self.assertEqual(result.exit_code, 0, f"{result.output}\n{result.exception}")
            legacy = db.session.get(Tenancy, 1)
            self.assertIsNone(legacy.water_price)
            self.assertEqual(legacy.contract_start, date(2020, 1, 15))
            self.assertIsNone(legacy.deposit_amount)
            self.assertIsNone(legacy.rent_price)
            self.assertEqual(db.session.get(Tenancy, 2).contract_start, date(2020, 1, 1))
            self.assertIsNone(db.session.get(Tenancy, 3).contract_start)
            self.assertEqual(len(legacy.occupants), 1)
            self.assertEqual(len(legacy.vehicles), 1)
            self.assertEqual(legacy.version, 2)
            for column, value in (("water_price", -1), ("service_price", -1), ("rent_price", -1), ("deposit_amount", -1), ("payment_day", 32)):
                with self.assertRaises(IntegrityError):
                    db.session.execute(db.text(f"UPDATE tenancy SET {column}=:value WHERE id=1"), {"value": value})
                    db.session.commit()
                db.session.rollback()
            self.assertEqual(db.session.execute(db.text("PRAGMA foreign_key_check")).all(), [])
            db.session.remove()
            db.engine.dispose()
