from datetime import date

from app.extensions import db
from app.models import ElectricityReading, MonthlyBill, ReadingRevision
from app.services.billing import reading_stamp
from test_v1 import AppTestCase


class BillingTests(AppTestCase):
    def setUp(self):
        super().setUp()
        self.login()
        self.room_obj = self.room(status="occupied", tenant_name="Example", occupants="Other")
        self.first = ElectricityReading(room_id=self.room_obj.id, period="2026-01", start_value=1250, end_value=1350, created_by=self.root_id)
        self.next = ElectricityReading(room_id=self.room_obj.id, period="2026-02", start_value=1350, end_value=1400, created_by=self.root_id)
        db.session.add_all([self.first, self.next])
        db.session.commit()

    def bill_data(self, reading=None, **extra):
        reading = reading or self.first
        tenant = self.room_obj.current_tenancy
        return {"action": "confirm", "period": reading.period, "tenancy_id": str(tenant.id), "tenancy_version": str(tenant.version),
                "stamp": reading_stamp(reading), "rent_price": "3000000", "water_price": "100000", "service_price": "150000", "electricity_price": "4000", "people_count": "2", "payment_day": "31", **extra}

    def correction_data(self, **extra):
        return {"action": "confirm", "stamp": reading_stamp(self.first), "start_value": "1250", "end_value": "1300", "reason": "Correct reading", **extra}

    def test_room_history_uses_saved_price_and_bill_override(self):
        path = f"/rooms/{self.room_obj.id}"
        self.first.electricity_price = 3600
        self.next.electricity_price = 0
        db.session.commit()
        html = self.client.get(path).get_data(as_text=True)
        self.assertIn('360.000', html)
        self.assertIn('<strong>0 ', html)
        self.room_obj.current_tenancy.electricity_price = 9000
        db.session.commit()
        self.assertIn('360.000', self.client.get(path).get_data(as_text=True))
        self.assertEqual(self.post(f"/rooms/{self.room_obj.id}/bill", self.bill_data()).status_code, 302)
        html = self.client.get(path).get_data(as_text=True)
        self.assertIn('400.000', html)
        self.assertNotIn('360.000', html)
        self.next.electricity_price = None
        db.session.commit()
        html = self.client.get(path).get_data(as_text=True)
        self.assertNotIn('450.000', html)

    def test_correction_updates_next_start_and_audits_both(self):
        data = self.correction_data(action="preview")
        path = f"/electricity/{self.first.id}/correct"
        self.assertEqual(self.post(path, data).status_code, 200)
        self.assertEqual(self.first.end_value, 1350)
        self.assertEqual(self.post(path, {**data, "action": "confirm"}).status_code, 302)
        self.assertEqual((self.first.consumption, self.next.consumption), (50, 100))
        self.assertEqual(self.next.end_value, 1400)
        self.assertEqual(db.session.scalar(db.select(db.func.count()).select_from(ReadingRevision)), 2)
        self.assertEqual(self.post(path, {**data, "action": "confirm"}).status_code, 400)

    def test_correction_rejects_negative_future_and_missing_reason(self):
        path = f"/electricity/{self.first.id}/correct"
        for extra in ({"end_value": "1249"}, {"end_value": "1401"}, {"end_value": "1.5"}, {"reason": ""}, {"stamp": "stale"}):
            self.assertEqual(self.post(path, self.correction_data(**extra)).status_code, 400)
        self.assertEqual(self.first.end_value, 1350)
        second = {"action": "confirm", "stamp": reading_stamp(self.next), "start_value": "1300", "end_value": "1450", "reason": "Wrong start"}
        self.assertEqual(self.post(f"/electricity/{self.next.id}/correct", second).status_code, 400)

    def test_snapshot_and_month_prices_are_independent(self):
        path = f"/rooms/{self.room_obj.id}/bill"
        self.assertEqual(self.post(path, self.bill_data(action="preview")).status_code, 200)
        self.assertEqual(db.session.scalar(db.select(db.func.count()).select_from(MonthlyBill)), 0)
        self.assertEqual(self.post(path, self.bill_data()).status_code, 302)
        first = db.session.scalar(db.select(MonthlyBill))
        self.assertEqual(first.total, 3750000)
        self.room_obj.current_tenancy.rent_price = 9000000
        db.session.commit()
        self.assertEqual(first.total, 3750000)
        self.assertEqual(self.post(path, self.bill_data(self.next, electricity_price="5000", rent_price="3200000")).status_code, 302)
        self.assertEqual(first.total, 3750000)
        self.assertEqual(self.post(path, self.bill_data()).status_code, 400)

    def test_room_price_change_updates_new_forms_not_existing_bills(self):
        from test_contracts import ContractTests
        path = f"/rooms/{self.room_obj.id}/bill"
        data = self.bill_data(self.next)
        self.assertEqual(self.post(path, self.bill_data()).status_code, 302)
        bill = db.session.scalar(db.select(MonthlyBill))
        payload = ContractTests.edit_data(self, self.room_obj, electricity_price="5000", water_price="120000", rent_price="3500000")
        self.assertEqual(self.post(f"/rooms/{self.room_obj.id}/edit", payload).status_code, 302)
        self.assertEqual((bill.electricity_price, bill.water_price, bill.rent_price, bill.total), (4000, 100000, 3000000, 3750000))
        self.assertEqual(self.post(path, data).status_code, 400)
        page = self.client.get(path + "?period=2026-02").get_data(as_text=True)
        for key, value in (("electricity_price", "5000"), ("water_price", "120000"), ("rent_price", "3500000")):
            self.assertRegex(page, 'name="' + key + '" value="' + value + '"')
        self.assertEqual(self.post(path, self.bill_data(self.next, electricity_price="5000", water_price="120000", rent_price="3500000")).status_code, 302)
        self.assertEqual(bill.total, 3750000)

    def test_billed_readings_require_root_cancel_and_keep_old_bill(self):
        path = f"/rooms/{self.room_obj.id}/bill"
        self.post(path, self.bill_data(self.next))
        bill = db.session.scalar(db.select(MonthlyBill))
        self.assertEqual(self.post(f"/electricity/{self.first.id}/correct", self.correction_data()).status_code, 400)
        self.assertEqual(self.next.start_value, 1350)
        other = self.app.test_client()
        self.login("manager", "AdminTest123!", other)
        self.assertEqual(self.post(f"/bills/{bill.id}/cancel", {"reason": "Fix"}, client=other).status_code, 403)
        self.assertEqual(self.post(f"/bills/{bill.id}/cancel", {"reason": "Fix"}).status_code, 302)
        self.assertIsNotNone(bill.cancelled_at)
        self.assertEqual(self.post(f"/electricity/{self.first.id}/correct", self.correction_data()).status_code, 302)
        self.assertEqual(bill.start_value, 1350)
        self.post(path, self.bill_data(self.next))
        self.assertEqual(db.session.scalar(db.select(db.func.count()).select_from(MonthlyBill)), 2)

    def test_invalid_prices_and_stale_inputs(self):
        path = f"/rooms/{self.room_obj.id}/bill"
        for extra in ({"electricity_price": ""}, {"water_price": "-1"}, {"electricity_price": "1.5"}, {"people_count": "0"}, {"payment_day": "32"}, {"tenancy_version": "99"}, {"tenancy_id": "999"}, {"stamp": "old"}):
            self.assertEqual(self.post(path, self.bill_data(**extra)).status_code, 400)
        self.assertEqual(self.post(path, self.bill_data(rent_price="0", water_price="0", service_price="0", electricity_price="0")).status_code, 302)
        self.assertEqual(db.session.scalar(db.select(MonthlyBill)).total, 0)

    def test_missing_reading_and_partial_month_are_blocked(self):
        path = f"/rooms/{self.room_obj.id}/bill"
        self.assertEqual(self.client.get(path + "?period=2026-03").status_code, 302)
        self.room_obj.current_tenancy.contract_start = date(2026, 1, 15)
        db.session.commit()
        self.assertEqual(self.post(path, self.bill_data()).status_code, 400)

    def test_pages_and_access(self):
        for path in ("/bills", "/bills?period=bad", f"/rooms/{self.room_obj.id}/bill?period=2026-01", f"/electricity/{self.first.id}/correct"):
            self.assertEqual(self.client.get(path).status_code, 200, path)
            self.assertEqual(self.app.test_client().get(path).status_code, 302)

    def test_reading_dates_and_amount_follow_correction_and_bill(self):
        page = self.client.get('/electricity/?period=2026-01').get_data(as_text=True)
        self.assertIn('Ngày chốt', page)
        self.assertIn('Cập nhật lần cuối', page)
        self.assertIn('400.000 đ', page)
        self.assertEqual(self.post(f'/electricity/{self.first.id}/correct', self.correction_data()).status_code, 302)
        page = self.client.get('/electricity/?period=2026-01').get_data(as_text=True)
        self.assertIn('200.000 đ', page)
        self.assertIn('Tạm tính', page)
        revision = db.session.scalar(db.select(ReadingRevision).where(ReadingRevision.reading_id == self.first.id))
        self.assertIn(self.app.jinja_env.filters['local_datetime'](revision.created_at), page)
        self.post(f'/rooms/{self.room_obj.id}/bill', self.bill_data(electricity_price='5000'))
        page = self.client.get('/electricity/?period=2026-01').get_data(as_text=True)
        self.assertIn('250.000 đ', page)
        self.assertIn('Đã chốt tiền', page)

    def test_saved_reading_keeps_rate_and_zero_is_valid(self):
        tenant = self.room_obj.current_tenancy
        self.assertEqual(self.post('/electricity/', {'period':'2026-03', f'end_{self.room_obj.id}':'1500'}).status_code, 302)
        reading = db.session.scalar(db.select(ElectricityReading).where(ElectricityReading.period == '2026-03'))
        self.assertEqual(reading.electricity_price, 4000)
        tenant.electricity_price = 6000
        db.session.commit()
        page = self.client.get('/electricity/?period=2026-03').get_data(as_text=True)
        self.assertIn('400.000 đ', page)
        self.assertNotIn('600.000 đ', page)
        tenant.electricity_price = 0
        db.session.commit()
        self.post('/electricity/', {'period':'2026-04', f'end_{self.room_obj.id}':'1600'})
        reading = db.session.scalar(db.select(ElectricityReading).where(ElectricityReading.period == '2026-04'))
        self.assertEqual(reading.electricity_price, 0)
