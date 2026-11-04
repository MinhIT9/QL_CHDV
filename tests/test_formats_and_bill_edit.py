import unittest
from datetime import datetime, timezone
from unittest.mock import patch
from sqlalchemy.exc import OperationalError

from app.extensions import db
from app.models import BillChange, ElectricityReading, MonthlyBill
from app.services.billing import bill_stamp
from app.services.queries import bill_change_query
from app.services.contracts import parse_date
from app.utils.formatting import business_date, local_datetime, money_input, parse_money, period_label, vnd
import test_bill_documents
from test_v1 import AppTestCase


class FormattingTests(unittest.TestCase):
    def test_money_roundtrip_zero_missing_grouping_and_limits(self):
        for value in (0, 1000000, 9223372036854775807):
            self.assertEqual(parse_money(vnd(value), 'Tiền', maximum=9223372036854775807), value)
        self.assertIsNone(parse_money('', 'Tiền'))
        self.assertEqual(money_input('1000000'), '1.000.000 đ')
        for value in ('1.23', '1,000', '-1000', '1e6', '1000.000', '1.000 đồng', '9' * 100):
            with self.assertRaises(ValueError):
                parse_money(value, 'Tiền')

    def test_vietnam_time_boundary_dates_and_periods(self):
        moment = datetime(2026, 10, 31, 18, 30, tzinfo=timezone.utc)
        self.assertEqual(local_datetime(moment).strftime('%d/%m/%Y %H:%M:%S'), '01/11/2026 01:30:00')
        self.assertEqual(local_datetime(moment.replace(tzinfo=None)), local_datetime(moment))
        self.assertEqual(parse_date('29/02/2024', 'Ngày'), parse_date('2024-02-29', 'Ngày'))
        self.assertEqual(business_date(parse_date('04/11/2026', 'Ngày')), '04/11/2026')
        self.assertEqual(period_label('2026-11'), '11/2026')
        for value in ('29/02/2025', '31/04/2026', '11/04/26'):
            with self.assertRaises(ValueError):
                parse_date(value, 'Ngày')


class BillEditTests(AppTestCase):
    data = test_bill_documents.BillDocumentTests.data
    create_bill = test_bill_documents.BillDocumentTests.create_bill

    def setUp(self):
        super().setUp()
        self.login()
        self.room_obj = self.room(status='occupied', tenant_name='Edit fixture')
        self.reading = ElectricityReading(room_id=self.room_obj.id, period='2026-01', start_value=100, end_value=277, created_by=self.root_id)
        db.session.add(self.reading)
        db.session.commit()
        self.original = self.create_bill()

    def edit_data(self, **extra):
        return {**self.data(), 'edit_stamp': bill_stamp(self.original), 'adjustment_reason': 'Correction fixture',
                'rent_price': '5.100.000 đ', 'final_amount': '', **extra}

    def test_preview_then_replace_keeps_snapshot_history_and_rejects_repeat(self):
        path = f'/bills/{self.original.id}/edit'
        self.room_obj.current_tenancy.rent_price = 1
        db.session.commit()
        values = self.edit_data(action='preview')
        self.assertEqual(self.post(path, values).status_code, 200)
        self.assertIsNone(self.original.cancelled_at)
        self.assertEqual(db.session.query(MonthlyBill).count(), 1)
        values['action'] = 'confirm'
        self.assertEqual(self.post(path, values).status_code, 302)
        replacement = db.session.scalar(db.select(MonthlyBill).where(MonthlyBill.cancelled_at.is_(None)))
        self.assertNotEqual(replacement.id, self.original.id)
        self.assertEqual(replacement.rent_price, 5100000)
        self.assertEqual(self.original.rent_price, 5000000)
        self.assertEqual(replacement.tenant_name, self.original.tenant_name)
        self.assertEqual(replacement.start_value, self.original.start_value)
        self.assertIn(f'#{replacement.id}', self.original.cancel_reason)
        self.assertEqual(self.post(path, values).status_code, 400)
        self.assertEqual(db.session.query(MonthlyBill).count(), 2)

    def test_paid_bill_and_stale_preview_are_blocked_on_server(self):
        path = f'/bills/{self.original.id}/edit'
        values = self.edit_data()
        self.post(f'/bills/{self.original.id}/receive', {'paid_date': '05/01/2026', 'receipt_version': '0'})
        self.assertEqual(self.client.get(path).status_code, 409)
        self.assertEqual(self.post(path, values).status_code, 400)
        self.assertEqual(db.session.query(MonthlyBill).count(), 1)
        self.assertEqual(db.session.query(BillChange).count(), 0)

    def test_admin_can_replace_unpaid_bill_and_reason_is_required(self):
        path = f'/bills/{self.original.id}/edit'
        self.post('/logout')
        self.login('manager', 'AdminTest123!')
        self.assertEqual(self.post(path, self.edit_data(adjustment_reason='')).status_code, 400)
        self.assertEqual(self.post(path, self.edit_data(final_amount='0 đ', adjustment_reason='Waive fixture')).status_code, 302)
        replacement = db.session.scalar(db.select(MonthlyBill).where(MonthlyBill.cancelled_at.is_(None)))
        self.assertEqual(replacement.total, 0)
        self.assertEqual(replacement.created_by, self.admin_id)

    def test_failed_commit_restores_active_original(self):
        with patch.object(db.session, 'commit', side_effect=OperationalError('fixture', {}, Exception('fixture'))):
            self.assertEqual(self.post(f'/bills/{self.original.id}/edit', self.edit_data()).status_code, 400)
        self.assertIsNone(self.original.cancelled_at)
        self.assertEqual(db.session.query(MonthlyBill).count(), 1)
        self.assertEqual(db.session.query(BillChange).count(), 0)

    def test_single_reason_is_required_for_price_change_even_if_total_is_fixed(self):
        path = f'/bills/{self.original.id}/edit'
        values = self.edit_data(final_amount=str(self.original.total), adjustment_reason='')
        self.assertEqual(self.post(path, values).status_code, 400)
        self.assertEqual(db.session.query(BillChange).count(), 0)
        values['adjustment_reason'] = 'Price corrected, agreed total retained'
        self.assertEqual(self.post(path, values).status_code, 302)
        log = db.session.scalar(db.select(BillChange))
        self.assertEqual(log.reason, values['adjustment_reason'])
        self.assertEqual(log.created_by, self.root_id)
        self.assertEqual(log.old_bill.rent_price, 5000000)
        self.assertEqual(log.new_bill.rent_price, 5100000)
        self.assertEqual(log.new_bill.total, log.old_bill.total)
        page = self.client.get(f'/bills/{log.new_bill_id}/edit').get_data(as_text=True)
        self.assertNotIn('name="edit_reason"', page)
        self.assertEqual(page.count('name="adjustment_reason"'), 1)
        self.assertIn('5.000.000 đ → 5.100.000 đ', page)
        self.assertIn(log.reason, page)

    def test_deadline_only_needs_no_reason_and_keeps_existing_adjustment(self):
        self.original.final_amount = self.original.total + 400
        self.original.adjustment_reason = 'Original rounding'
        db.session.commit()
        values = self.edit_data(rent_price=str(self.original.rent_price), final_amount=str(self.original.total),
                                adjustment_reason='', payment_day='6')
        self.assertEqual(self.post(f'/bills/{self.original.id}/edit', values).status_code, 302)
        log = db.session.scalar(db.select(BillChange))
        self.assertEqual(log.reason, '')
        self.assertEqual(log.new_bill.adjustment_reason, 'Original rounding')
        self.assertEqual(log.new_bill.total, self.original.total)
        self.assertEqual(log.new_bill.due_date.day, 6)
        room = self.client.get(f'/rooms/{self.room_obj.id}').get_data(as_text=True)
        self.assertIn('05/01/2026 → 06/01/2026', room)

    def test_repeated_changes_remain_in_same_period_journal(self):
        self.post(f'/bills/{self.original.id}/edit', self.edit_data())
        middle = db.session.scalar(db.select(MonthlyBill).where(MonthlyBill.cancelled_at.is_(None)))
        values = self.edit_data(edit_stamp=bill_stamp(middle), rent_price='5200000', adjustment_reason='Second correction')
        self.assertEqual(self.post(f'/bills/{middle.id}/edit', values).status_code, 302)
        newest = db.session.scalar(db.select(MonthlyBill).where(MonthlyBill.cancelled_at.is_(None)))
        self.assertEqual(db.session.query(BillChange).count(), 2)
        page = self.client.get(f'/bills/{newest.id}/edit').get_data(as_text=True)
        self.assertIn('Correction fixture', page)
        self.assertIn('Second correction', page)
        records = db.session.scalars(bill_change_query(self.room_obj.id, '2026-01')).all()
        self.assertEqual([record.new_bill_id for record in records], [newest.id, middle.id])
