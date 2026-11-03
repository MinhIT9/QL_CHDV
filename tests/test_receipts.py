from datetime import date

from app.extensions import db
from app.models import MonthlyBill, Receipt
from test_v1 import AppTestCase


class ReceiptTests(AppTestCase):
    def setUp(self):
        super().setUp()
        self.login()
        self.bills = []
        for code in ('P101', 'P102'):
            room = self.room(code, status='occupied', tenant_name='Example')
            bill = MonthlyBill(room_id=room.id, tenancy_id=room.current_tenancy.id, period='2026-01',
                               room_code=code, tenant_name='Example', start_value=100, end_value=200,
                               rent_price=3000000, water_price=100000, service_price=150000,
                               electricity_price=4000, people_count=2, due_date=date(2026, 1, 31), created_by=self.root_id)
            db.session.add(bill)
            self.bills.append(bill)
        db.session.commit()

    def pay(self, bill, **extra):
        return self.post(f'/bills/{bill.id}/receive', {'paid_date':'2026-01-05', 'note':'Received in full', 'receipt_version':str(bill.receipts[-1].id if bill.receipts else 0), **extra})

    def test_receive_records_full_amount_date_author_and_moves_down(self):
        first, second = self.bills
        self.assertEqual(self.pay(first, amount='1').status_code, 302)
        receipt = first.paid_receipt
        self.assertEqual(receipt.amount, first.total)
        self.assertEqual(receipt.paid_date, date(2026, 1, 5))
        self.assertEqual(receipt.created_by, self.root_id)
        page = self.client.get('/bills?period=2026-01').get_data(as_text=True)
        self.assertLess(page.index(f'Phiếu #{second.id}'), page.index(f'Phiếu #{first.id}'))
        self.pay(first)
        self.assertEqual(db.session.scalar(db.select(db.func.count()).select_from(Receipt)), 1)

    def test_paid_bill_cannot_be_cancelled_and_root_can_reverse_with_history(self):
        bill = self.bills[0]
        self.pay(bill)
        receipt = bill.paid_receipt
        self.post(f'/bills/{bill.id}/cancel', {'reason':'Mistake'})
        self.assertIsNone(bill.cancelled_at)
        other = self.app.test_client()
        self.login('manager', 'AdminTest123!', other)
        self.assertEqual(self.post(f'/receipts/{receipt.id}/reverse', {'reason':'Mistake'}, client=other).status_code, 403)
        self.post(f'/receipts/{receipt.id}/reverse', {'reason':''})
        self.assertIsNone(receipt.reversed_at)
        self.post(f'/receipts/{receipt.id}/reverse', {'reason':'Incorrect confirmation'})
        self.assertIsNone(bill.paid_receipt)
        self.assertEqual(receipt.reversed_by, self.root_id)
        self.assertEqual(receipt.amount, bill.total)
        self.pay(bill)
        self.assertEqual(len(bill.receipts), 2)
        self.assertIsNotNone(bill.paid_receipt)

    def test_admin_can_receive_and_invalid_dates_or_cancelled_bills_are_rejected(self):
        bill = self.bills[0]
        for value in ('', '2999-01-01', '2026-02-30'):
            self.pay(bill, paid_date=value)
            self.assertIsNone(bill.paid_receipt)
        self.post(f'/bills/{bill.id}/cancel', {'reason':'Incorrect bill'})
        self.pay(bill)
        self.assertIsNone(bill.paid_receipt)
        other = self.app.test_client()
        self.login('manager', 'AdminTest123!', other)
        response = self.post(f'/bills/{self.bills[1].id}/receive', {'paid_date':'2026-01-05', 'receipt_version':'0'}, client=other)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.bills[1].paid_receipt.created_by, self.admin_id)

    def test_room_filters_and_month_isolation(self):
        first, second = self.bills
        self.pay(first)
        paid = self.client.get('/?period=2026-01&payment=paid').get_data(as_text=True)
        self.assertIn('P101', paid)
        self.assertNotIn('P102', paid)
        unpaid = self.client.get('/?period=2026-01&payment=unpaid').get_data(as_text=True)
        self.assertNotIn('P101', unpaid)
        self.assertIn('P102', unpaid)
        february = self.client.get('/?period=2026-02&payment=paid').get_data(as_text=True)
        self.assertNotIn('P101', february)
        self.assertIn('Chưa chốt', self.client.get('/?period=2026-02').get_data(as_text=True))
        full = self.client.get('/?period=2026-01&view=full').get_data(as_text=True)
        self.assertIn('Tiền cọc', full)
        compact = self.client.get('/?period=2026-01').get_data(as_text=True)
        self.assertNotIn('<th>Tiền cọc', compact)
        self.assertLess(compact.index('P101'), compact.index('P102'))

    def test_undo_then_cancel_keeps_receipt_history_and_zero_bill(self):
        bill = self.bills[0]
        bill.rent_price = bill.water_price = bill.service_price = bill.electricity_price = 0
        db.session.commit()
        self.pay(bill)
        receipt = bill.paid_receipt
        self.assertEqual(receipt.amount, 0)
        self.post(f'/receipts/{receipt.id}/reverse', {'reason':'Mistake'})
        self.pay(bill, receipt_version='0')
        self.assertIsNone(bill.paid_receipt)
        self.post(f'/bills/{bill.id}/cancel', {'reason':'Replace bill'})
        self.assertIsNotNone(bill.cancelled_at)
        self.assertEqual(len(bill.receipts), 1)
        self.assertIsNotNone(receipt.reversed_at)
