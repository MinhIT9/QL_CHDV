from datetime import date
from pathlib import Path

from app import create_app
from app.extensions import db
from app.models import ElectricityReading, MonthlyBill, Receipt, Room, User
from app.services.billing import amount_in_words, reading_stamp
from test_v1 import AppTestCase


class BillDocumentTests(AppTestCase):
    def setUp(self):
        super().setUp()
        self.login()
        self.room_obj = self.room(status='occupied', tenant_name='Receipt fixture')
        self.reading = ElectricityReading(room_id=self.room_obj.id, period='2026-01', start_value=100, end_value=277, created_by=self.root_id)
        db.session.add(self.reading)
        db.session.commit()

    def data(self, **extra):
        tenant = self.room_obj.current_tenancy
        return {'action': 'confirm', 'period': '2026-01', 'tenancy_id': str(tenant.id), 'tenancy_version': str(tenant.version),
                'stamp': reading_stamp(self.reading), 'rent_price': '5000000', 'water_price': '100000', 'service_price': '150000',
                'electricity_price': '3800', 'people_count': '2', 'payment_day': '5', **extra}

    def create_bill(self, **extra):
        response = self.post(f'/rooms/{self.room_obj.id}/bill', self.data(**extra))
        self.assertEqual(response.status_code, 302, response.get_data(as_text=True))
        return db.session.scalar(db.select(MonthlyBill).where(MonthlyBill.cancelled_at.is_(None)))

    def test_adjustment_preview_snapshot_and_receive_use_final_total(self):
        data = self.data(action='preview', final_amount='6023000', adjustment_reason='Round up')
        response = self.post(f'/rooms/{self.room_obj.id}/bill', data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('6.023.000', response.get_data(as_text=True))
        self.assertEqual(db.session.query(MonthlyBill).count(), 0)
        bill = self.create_bill(final_amount='6023000', adjustment_reason='Round up')
        self.assertEqual((bill.computed_total, bill.total, bill.adjustment_amount), (6022600, 6023000, 400))
        self.room_obj.current_tenancy.rent_price = 1
        db.session.commit()
        self.assertEqual(bill.total, 6023000)
        self.post(f'/bills/{bill.id}/receive', {'paid_date': '2026-01-05', 'receipt_version': '0', 'amount': '1'})
        self.assertEqual(bill.paid_receipt.amount, 6023000)
        html = self.client.get(f'/bills/{bill.id}').get_data(as_text=True)
        self.assertIn('ĐÃ THANH TOÁN', html)
        self.assertIn('PHIẾU THU TIỀN', html)
        self.assertIn('Round up', html)
        self.assertIn('6.023.000', html)

    def test_adjustment_validation_and_zero(self):
        for extra in ({'final_amount': '1'}, {'final_amount': '-1', 'adjustment_reason': 'bad'},
                      {'final_amount': '1.5', 'adjustment_reason': 'bad'}, {'final_amount': '9223372036854775808', 'adjustment_reason': 'bad'},
                      {'final_amount': '1', 'adjustment_reason': ' '}, {'final_amount': '1', 'adjustment_reason': 'x' * 501}):
            response = self.post(f'/rooms/{self.room_obj.id}/bill', self.data(**extra))
            self.assertEqual(response.status_code, 400)
            self.assertEqual(db.session.query(MonthlyBill).count(), 0)
        bill = self.create_bill(final_amount='0', adjustment_reason='Waived')
        self.assertEqual(bill.total, 0)
        self.assertEqual(bill.adjustment_amount, -6022600)
        self.post(f'/bills/{bill.id}/receive', {'paid_date': '2026-01-05', 'receipt_version': '0'})
        self.assertEqual(bill.paid_receipt.amount, 0)

    def test_unadjusted_final_default_and_document_access(self):
        bill = self.create_bill()
        self.assertEqual(bill.total, bill.computed_total)
        self.assertEqual(bill.adjustment_reason, '')
        path = f'/bills/{bill.id}'
        self.assertEqual(self.app.test_client().get(path).status_code, 302)
        html = self.client.get(path).get_data(as_text=True)
        self.assertIn('CHƯA THANH TOÁN', html)
        self.assertNotIn('id="sidebar"', html)
        self.assertIn('print-receipt', html)
        self.assertIn('save-receipt', html)
        self.assertNotIn('Bằng chữ:', html)
        self.assertIn('hx-boost="false"', self.client.get('/bills?period=2026-01').get_data(as_text=True))
        self.assertEqual(self.client.get('/bills/999999').status_code, 404)

    def test_room_history_includes_cancelled_and_reissued_bill_for_same_period(self):
        original = self.create_bill(final_amount='6000000', adjustment_reason='Discount')
        original_id = original.id
        self.post(f'/bills/{original.id}/cancel', {'reason': 'Reissue'})
        replacement = self.create_bill()
        html = self.client.get(f'/rooms/{self.room_obj.id}').get_data(as_text=True)
        self.assertIn('Lịch sử chốt tiền', html)
        self.assertIn(f'/bills/{original_id}', html)
        self.assertIn(f'/bills/{replacement.id}', html)
        self.assertIn('Discount', html)
        self.assertIn('Đã hủy hiệu lực', html)
        self.assertLess(html.index(f'/bills/{replacement.id}'), html.index(f'/bills/{original_id}'))
        cancelled = self.client.get(f'/bills/{original_id}').get_data(as_text=True)
        self.assertIn('ĐÃ HỦY HIỆU LỰC', cancelled)
        self.assertNotIn('CHƯA THANH TOÁN', cancelled)

    def test_vietnamese_amount_words(self):
        for number, text in ((0, 'Không đồng'), (15, 'Mười lăm đồng'), (21, 'Hai mươi mốt đồng'),
                             (1005, 'Một nghìn không trăm lẻ năm đồng'),
                             (5011600, 'Năm triệu không trăm mười một nghìn sáu trăm đồng')):
            self.assertEqual(amount_in_words(number), text)

    def test_migration_keeps_legacy_paid_bill_and_amount(self):
        app = create_app({'TESTING': True, 'SECRET_KEY': 'migration-only',
                          'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + (Path(self.temp.name) / 'legacy-bill.sqlite3').as_posix()})
        with app.app_context():
            try:
                result = app.test_cli_runner().invoke(args=['db', 'upgrade', 'a24d09e86c31'])
                self.assertEqual(result.exit_code, 0, result.output)
                # Copy a fixture snapshot into the pre-upgrade table using SQL, not the new ORM columns.
                db.session.execute(db.text("INSERT INTO user(id,username,password_hash,is_root,enabled,must_change_password,session_token,failed_logins,created_at) VALUES (1,'fixture','unused',1,1,0,'fixture-token',0,'2026-01-01')"))
                db.session.execute(db.text("INSERT INTO room(id,code,active,note) VALUES (1,'OLD',1,'')"))
                db.session.execute(db.text("INSERT INTO tenancy(id,room_id,tenant_name,started_at,version) VALUES (1,1,'Fixture','2026-01-01',1)"))
                db.session.execute(db.text("INSERT INTO monthly_bill(id,room_id,tenancy_id,period,tenant_name,room_code,start_value,end_value,rent_price,water_price,service_price,electricity_price,people_count,due_date,created_by,created_at) VALUES (1,1,1,'2026-01','Fixture','OLD',0,10,1000,100,50,10,2,'2026-01-05',1,'2026-01-01')"))
                db.session.execute(db.text("INSERT INTO receipt(bill_id,amount,paid_date,note,created_by,created_at) VALUES (1,1350,'2026-01-05','',1,'2026-01-05')"))
                db.session.commit()
                result = app.test_cli_runner().invoke(args=['db', 'upgrade'])
                self.assertEqual(result.exit_code, 0, result.output)
                bill = db.session.get(MonthlyBill, 1)
                self.assertIsNone(bill.final_amount)
                self.assertEqual((bill.total, bill.paid_receipt.amount), (1350, 1350))
            finally:
                db.session.remove()
                db.engine.dispose()
