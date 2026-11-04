import calendar
import hashlib
from datetime import date

from app.extensions import db
from app.models import BillChange, ElectricityReading, MonthlyBill, Photo, ReadingRevision, utcnow
from app.services.contracts import parse_integer
from app.utils.formatting import business_date, parse_money, vnd
from app.services.electricity import current_period, integer_reading, valid_period
from app.services.photos import stage_photo, upload_batch

BILL_PRICES = (('rent_price', 'Tiền phòng'), ('water_price', 'Giá nước'),
               ('service_price', 'Dịch vụ'), ('electricity_price', 'Đơn giá điện'))


def bill_prices(data):
    return {key: parse_money(data.get(key, ''), label, required=True) for key, label in BILL_PRICES}


def lock_writes():
    if db.engine.dialect.name == "sqlite":
        db.session.execute(db.text("BEGIN IMMEDIATE"))
    db.session.expire_all()


def reading_pair(reading):
    rows = db.session.scalars(db.select(ElectricityReading).where(ElectricityReading.room_id == reading.room_id).order_by(ElectricityReading.period)).all()
    index = rows.index(reading)
    return rows[index - 1] if index else None, rows[index + 1] if index + 1 < len(rows) else None


def reading_stamp(reading):
    previous, following = reading_pair(reading)
    values = [(r.id, r.start_value, r.end_value) for r in (previous, reading, following) if r]
    return hashlib.sha256(str(values).encode()).hexdigest()


def correction(reading, data, user_id, save=False, upload=None):
    if save:
        lock_writes()
    if data.get("stamp") != reading_stamp(reading):
        raise ValueError("Số điện vừa thay đổi. Hãy tải lại và xem trước lại.")
    previous, following = reading_pair(reading)
    start = integer_reading(data.get("start_value", ""), "Chỉ số đầu")
    end = integer_reading(data.get("end_value", ""), "Chỉ số cuối")
    reason = data.get("reason", "").strip()
    if not reason or len(reason) > 500:
        raise ValueError("Cần lý do điều chỉnh, tối đa 500 ký tự.")
    if end < start or (previous and start != previous.end_value) or (following and end > following.end_value):
        raise ValueError("Chỉ số không khớp kỳ trước/kỳ sau hoặc cuối nhỏ hơn đầu. Hãy đối chiếu lại đồng hồ.")
    changes = [(reading, start, end)]
    if following and following.start_value != end:
        changes.append((following, end, following.end_value))
    changes = [(r, a, b) for r, a, b in changes if (r.start_value, r.end_value) != (a, b)]
    if not changes:
        raise ValueError("Chỉ số mới không thay đổi.")
    periods = [r.period for r, _, _ in changes]
    if db.session.scalar(db.select(MonthlyBill.id).where(MonthlyBill.room_id == reading.room_id, MonthlyBill.period.in_(periods), MonthlyBill.cancelled_at.is_(None))):
        raise ValueError("Có phiếu tiền đã chốt trong các kỳ bị ảnh hưởng. Root cần hủy phiếu với lý do trước khi sửa điện.")
    preview = [{"period": r.period, "old_start": r.start_value, "old_end": r.end_value, "new_start": a, "new_end": b} for r, a, b in changes]
    if save:
        with upload_batch() as staged:
            if upload and upload.filename:
                stage_photo(upload, user_id, staged, reading=reading)
            for r, a, b in changes:
                db.session.add(ReadingRevision(reading_id=r.id, old_start=r.start_value, old_end=r.end_value, new_start=a, new_end=b, reason=reason, created_by=user_id))
                r.start_value, r.end_value = a, b
            db.session.commit()
    return preview


def bill_tenancy(room, period):
    if not valid_period(period) or period > current_period():
        raise ValueError("Kỳ tháng không hợp lệ hoặc trong tương lai.")
    year, month = map(int, period.split("-"))
    first, last = date(year, month, 1), date(year, month, calendar.monthrange(year, month)[1])
    if any((t.contract_start is None or (t.ended_at and t.move_out_date is None)) and (t.move_out_date is None or t.move_out_date >= first) for t in room.tenancies):
        raise ValueError("Cần bổ sung ngày hợp đồng/trả phòng của các đợt thuê liên quan trước khi chốt tiền.")
    tenants = [t for t in room.tenancies if t.contract_start and t.contract_start <= last and (t.move_out_date is None or t.move_out_date >= first)]
    if len(tenants) != 1:
        raise ValueError("Kỳ này chưa xác định được một đợt thuê duy nhất. Kiểm tra ngày hợp đồng/đổi khách.")
    tenant = tenants[0]
    if tenant.contract_start > first or (tenant.move_out_date and tenant.move_out_date < last):
        raise ValueError("Chưa hỗ trợ tính tiền kỳ vào/trả phòng giữa tháng.")
    return tenant


def bill_values(room, period, data, user_id, save=False):
    if save:
        lock_writes()
    tenant = bill_tenancy(room, period)
    reading = db.session.scalar(db.select(ElectricityReading).where(ElectricityReading.room_id == room.id, ElectricityReading.period == period))
    if not reading:
        raise ValueError("Cần lưu số điện của kỳ này trước khi chốt tiền.")
    if save and db.session.scalar(db.select(Photo.id).where(Photo.reading_id == reading.id, Photo.status == "pending")):
        raise ValueError("Ảnh công tơ đang xử lý. Chờ hoàn tất trước khi chốt phiếu tiền.")
    if data.get("tenancy_id") != str(tenant.id) or data.get("tenancy_version") != str(tenant.version) or data.get("stamp") != reading_stamp(reading):
        raise ValueError("Thông tin khách hoặc số điện đã thay đổi. Hãy tải lại và xem trước.")
    if db.session.scalar(db.select(MonthlyBill.id).where(MonthlyBill.room_id == room.id, MonthlyBill.period == period, MonthlyBill.cancelled_at.is_(None))):
        raise ValueError("Phòng đã có phiếu tiền có hiệu lực trong kỳ này.")
    values = bill_prices(data)
    values["people_count"] = parse_integer(data.get("people_count", ""), "Số người tính nước", 1, 31, True)
    payment_day = parse_integer(data.get("payment_day", ""), "Ngày đến hạn", 1, 31, True)
    year, month = map(int, period.split("-"))
    values.update(room_id=room.id, tenancy_id=tenant.id, period=period, room_code=room.code, tenant_name=tenant.tenant_name,
                  start_value=reading.start_value, end_value=reading.end_value, created_by=user_id,
                  due_date=date(year, month, min(payment_day, calendar.monthrange(year, month)[1])))
    bill = MonthlyBill(**values)
    apply_final_amount(bill, data)
    if save:
        db.session.add(bill)
        db.session.commit()
    return bill



def apply_final_amount(bill, data, require_reason=True):
    final = parse_money(data.get('final_amount', '').strip(), 'Số tiền thu cuối cùng', maximum=9_223_372_036_854_775_807)
    bill.final_amount = final if final is not None else bill.computed_total
    bill.adjustment_reason = data.get('adjustment_reason', '').strip()
    if len(bill.adjustment_reason) > 500 or (require_reason and bill.adjustment_amount != 0 and not bill.adjustment_reason):
        raise ValueError('Điều chỉnh tổng tiền cần lý do, tối đa 500 ký tự.')


def bill_stamp(bill):
    fields = ('id', 'rent_price', 'water_price', 'service_price', 'electricity_price', 'people_count',
              'final_amount', 'adjustment_reason', 'due_date', 'cancelled_at')
    state = [getattr(bill, key) for key in fields]
    state += [(r.id, r.reversed_at) for r in bill.receipts]
    return hashlib.sha256(str(state).encode()).hexdigest()


def edit_bill(original, data, user_id, save=False):
    if save:
        lock_writes()
    if original.cancelled_at or original.paid_receipt:
        raise ValueError('Chỉ sửa phiếu chưa thu và còn hiệu lực.')
    if data.get('edit_stamp') != bill_stamp(original):
        raise ValueError('Phiếu hoặc lịch sử thu đã thay đổi. Hãy tải lại trang.')
    fields = ('room_id', 'tenancy_id', 'period', 'room_code', 'tenant_name', 'start_value', 'end_value')
    values = {key: getattr(original, key) for key in fields}
    values.update(bill_prices(data))
    values['people_count'] = parse_integer(data.get('people_count', ''), 'Số người tính nước', 1, 31, True)
    day = parse_integer(data.get('payment_day', ''), 'Ngày đến hạn', 1, 31, True)
    year, month = map(int, original.period.split('-'))
    values['due_date'] = date(year, month, min(day, calendar.monthrange(year, month)[1]))
    bill = MonthlyBill(**values, created_by=user_id)
    apply_final_amount(bill, data, require_reason=False)
    reason = bill.adjustment_reason
    price_changed = any(getattr(original, key) != getattr(bill, key) for key, _ in BILL_PRICES) or original.total != bill.total
    if price_changed and not reason:
        raise ValueError('Cần lý do sửa giá khi thay đổi giá hoặc số tiền thu.')
    if not reason:
        bill.adjustment_reason = original.adjustment_reason
    changed = ('rent_price', 'water_price', 'service_price', 'electricity_price', 'people_count', 'due_date', 'adjustment_reason')
    if all(getattr(original, key) == getattr(bill, key) for key in changed) and original.total == bill.total:
        raise ValueError('Phiếu mới chưa có thay đổi.')
    if save:
        original.cancelled_at, original.cancelled_by = utcnow(), user_id
        original.cancel_reason = 'Đang thay thế phiếu'
        db.session.flush()  # Release the active room/period unique key before inserting replacement.
        db.session.add(bill)
        db.session.flush()
        original.cancel_reason = f'Thay bằng phiếu #{bill.id}' + (f': {reason[:450]}' if reason else '')
        db.session.add(BillChange(old_bill=original, new_bill=bill, reason=reason, created_by=user_id))
        db.session.commit()
    return bill


def change_history_rows(records):
    fields = [(key, label, vnd) for key, label in BILL_PRICES] + [
        ('people_count', 'Số người tính nước', str), ('due_date', 'Ngày đến hạn', business_date),
        ('computed_total', 'Tổng tự tính', vnd), ('total', 'Tiền thu cuối cùng', vnd),
        ('adjustment_reason', 'Lý do giá trên phiếu', lambda value: value or '—')]
    return [{'record': record, 'changes': [
        {'label': label, 'before': formatter(getattr(record.old_bill, key)), 'after': formatter(getattr(record.new_bill, key))}
        for key, label, formatter in fields if getattr(record.old_bill, key) != getattr(record.new_bill, key)
    ]} for record in records]

def amount_in_words(amount):
    """Spell non-negative integer VND without floating-point arithmetic."""
    digits = ('không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín')
    units = ('', 'nghìn', 'triệu', 'tỷ', 'nghìn tỷ', 'triệu tỷ', 'tỷ tỷ')
    if amount == 0:
        return 'Không đồng'
    groups = []
    while amount:
        groups.append(amount % 1000)
        amount //= 1000
    result = []
    for index in range(len(groups) - 1, -1, -1):
        number = groups[index]
        if not number:
            continue
        hundreds, remainder = divmod(number, 100)
        tens, ones = divmod(remainder, 10)
        words = []
        if hundreds or result:
            words.extend((digits[hundreds], 'trăm'))
        if tens >= 2:
            words.extend((digits[tens], 'mươi'))
        elif tens == 1:
            words.append('mười')
        elif ones and (hundreds or result):
            words.append('lẻ')
        if ones:
            words.append('mốt' if ones == 1 and tens >= 2 else 'lăm' if ones == 5 and tens else digits[ones])
        if units[index]:
            words.append(units[index])
        result.extend(words)
    return (' '.join(result) + ' đồng').capitalize()
