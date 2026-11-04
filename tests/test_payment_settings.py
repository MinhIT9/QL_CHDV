from io import BytesIO

from PIL import Image

from app.extensions import db
from app.models import PaymentSettings, ElectricityReading
from app.services.payment_settings import qr_path
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
        return dict(bank_name='Fixture bank', account_number='0012345678', account_name='FIXTURE OWNER', note='Room and month', **extra)

    def qr_upload(self):
        stream = BytesIO()
        Image.new('RGB', (180, 180), 'white').save(stream, 'PNG')
        stream.seek(0)
        return stream, 'qr.png'

    def test_save_replace_remove_and_receipt_visibility(self):
        response = self.post('/settings/payment', self.payment_data(qr=self.qr_upload()))
        self.assertEqual(response.status_code, 302)
        settings = db.session.get(PaymentSettings, 1)
        old_token = settings.qr_token
        self.assertTrue(qr_path(old_token).is_file())
        with self.client.get('/settings/payment/qr/' + old_token) as response:
            self.assertEqual(response.mimetype, 'image/png')
        bill = self.create_bill()
        html = self.client.get(f'/bills/{bill.id}').get_data(as_text=True)
        self.assertIn('0012345678', html)
        self.assertIn(old_token, html)
        self.post('/settings/payment', self.payment_data(qr=self.qr_upload()))
        self.assertNotEqual(settings.qr_token, old_token)
        self.assertFalse(qr_path(old_token).exists())
        self.assertEqual(self.client.get('/settings/payment/qr/' + old_token).status_code, 404)
        self.post(f'/bills/{bill.id}/receive', {'paid_date': '2026-01-05', 'receipt_version': '0'})
        self.assertNotIn('Thông tin chuyển khoản', self.client.get(f'/bills/{bill.id}').get_data(as_text=True))
        self.post('/settings/payment', self.payment_data(remove_qr='1'))
        self.assertIsNone(settings.qr_token)

    def test_admin_access_validation_and_csrf(self):
        self.post('/logout')
        self.assertEqual(self.client.get('/settings/payment').status_code, 302)
        self.login('manager', 'AdminTest123!')
        self.assertEqual(self.client.get('/settings/payment').status_code, 200)
        self.assertEqual(self.client.post('/settings/payment', data=self.payment_data()).status_code, 400)
        self.assertEqual(self.post('/settings/payment', self.payment_data()).status_code, 302)
        self.assertEqual(self.post('/settings/payment', self.payment_data(qr=(BytesIO(b'bad'), 'qr.png'))).status_code, 400)
        values = self.payment_data()
        values['bank_name'] = ''
        self.assertEqual(self.post('/settings/payment', values).status_code, 400)
        self.assertEqual(db.session.get(PaymentSettings, 1).bank_name, 'Fixture bank')
