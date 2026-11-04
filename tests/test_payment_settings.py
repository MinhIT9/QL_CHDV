from io import BytesIO
from unittest.mock import patch

from PIL import Image

from app.extensions import db
from app.models import PaymentSettings, ElectricityReading
from app.services.vietqr import qr_png
import test_bill_documents
from test_v1 import AppTestCase


class PaymentSettingsTests(AppTestCase):
    data = test_bill_documents.BillDocumentTests.data
    create_bill = test_bill_documents.BillDocumentTests.create_bill

    def setUp(self):
        super().setUp()
        self.login()
        self.room_obj = self.room(status='occupied', tenant_name='Payment fixture')
        self.reading = ElectricityReading(room_id=self.room_obj.id, period='2026-01', start_value=100, end_value=277, created_by=self.root_id)
        db.session.add(self.reading)
        db.session.commit()

    def payment_data(self, **extra):
        values = dict(bank_bin='970436', account_number='0012345678', account_name='FIXTURE OWNER', note='Room and month', auto_transfer_content='1')
        return {**values, **extra}

    def test_generated_qr_uses_final_bill_and_hides_after_payment(self):
        response = self.post('/settings/payment', self.payment_data())
        self.assertEqual(response.status_code, 302)
        settings = db.session.get(PaymentSettings, 1)
        self.assertEqual(settings.bank_name, 'Vietcombank')
        self.assertEqual(settings.account_number, '0012345678')
        with self.client.get('/settings/payment/qr') as response:
            self.assertEqual(response.mimetype, 'image/png')
            with Image.open(BytesIO(response.data)) as image:
                self.assertEqual(image.width, image.height)
        bill = self.create_bill(final_amount='6231000', adjustment_reason='Round fixture')
        html = self.client.get(f'/bills/{bill.id}').get_data(as_text=True)
        self.assertIn(f'/bills/{bill.id}/qr', html)
        self.assertIn('0012345678', html)
        with self.client.get(f'/bills/{bill.id}/qr?amount=1&account=wrong') as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers['Cache-Control'], 'no-store')
        self.post(f'/bills/{bill.id}/receive', {'paid_date': '2026-01-05', 'receipt_version': '0'})
        self.assertNotIn('Thông tin chuyển khoản', self.client.get(f'/bills/{bill.id}').get_data(as_text=True))
        self.assertEqual(self.client.get(f'/bills/{bill.id}/qr').status_code, 404)

    def test_admin_access_validation_and_csrf(self):
        self.post('/logout')
        self.assertEqual(self.client.get('/settings/payment').status_code, 302)
        self.assertEqual(self.client.get('/settings/payment/qr').status_code, 302)
        self.login('manager', 'AdminTest123!')
        self.assertEqual(self.client.get('/settings/payment').status_code, 200)
        self.assertEqual(self.client.post('/settings/payment', data=self.payment_data()).status_code, 400)
        self.assertEqual(self.post('/settings/payment', self.payment_data()).status_code, 302)
        for extra in ({'bank_bin':'999999'}, {'account_number':'123 456'}, {'account_number':'1'*20}, {'account_name':''}):
            self.assertEqual(self.post('/settings/payment', self.payment_data(**extra)).status_code, 400)
        self.assertEqual(db.session.get(PaymentSettings, 1).bank_bin, '970436')

    def test_content_switch_changes_payload_and_document_but_keeps_amount(self):
        self.post('/settings/payment', self.payment_data())
        bill = self.create_bill()
        for enabled in (False, True):
            values = self.payment_data()
            if not enabled:
                values.pop('auto_transfer_content')
            self.assertEqual(self.post('/settings/payment', values).status_code, 302)
            self.assertEqual(db.session.get(PaymentSettings, 1).auto_transfer_content, enabled)
            with patch('app.electricity.billing_routes.qr_png', wraps=qr_png) as render:
                with self.client.get(f'/bills/{bill.id}/qr') as response:
                    self.assertEqual(response.status_code, 200)
                value = render.call_args.args[0]
            tags = {}
            position = 0
            while position < len(value):
                tag, length = value[position:position+2], int(value[position+2:position+4])
                tags[tag] = value[position+4:position+4+length]
                position += 4 + length
            self.assertEqual(tags['54'], str(bill.total))
            self.assertEqual('62' in tags, enabled)
            html = self.client.get(f'/bills/{bill.id}').get_data(as_text=True)
            self.assertEqual('Nội dung: <strong>' in html, enabled)

    def test_zero_cancelled_and_excessive_amount_do_not_generate_qr(self):
        self.post('/settings/payment', self.payment_data())
        bill = self.create_bill(final_amount='0', adjustment_reason='Waive fixture')
        self.assertEqual(self.client.get(f'/bills/{bill.id}/qr').status_code, 404)
        self.assertNotIn(f'/bills/{bill.id}/qr', self.client.get(f'/bills/{bill.id}').get_data(as_text=True))
        self.post(f'/bills/{bill.id}/cancel', {'reason':'Replace fixture'})
        self.assertEqual(self.client.get(f'/bills/{bill.id}/qr').status_code, 404)
        replacement = self.create_bill(final_amount='10000000000000', adjustment_reason='Large fixture')
        self.assertEqual(self.client.get(f'/bills/{replacement.id}/qr').status_code, 404)
        self.assertEqual(self.client.get(f'/bills/{replacement.id}').status_code, 200)
