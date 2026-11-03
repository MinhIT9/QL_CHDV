import calendar
import hashlib
from datetime import date

from app.extensions import db
from app.models import ElectricityReading, MonthlyBill, ReadingRevision, utcnow
from app.services.contracts import parse_integer
from app.services.electricity import current_period, integer_reading, valid_period


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


def correction(reading, data, user_id, save=False):
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
    if data.get("tenancy_id") != str(tenant.id) or data.get("tenancy_version") != str(tenant.version) or data.get("stamp") != reading_stamp(reading):
        raise ValueError("Thông tin khách hoặc số điện đã thay đổi. Hãy tải lại và xem trước.")
    if db.session.scalar(db.select(MonthlyBill.id).where(MonthlyBill.room_id == room.id, MonthlyBill.period == period, MonthlyBill.cancelled_at.is_(None))):
        raise ValueError("Phòng đã có phiếu tiền có hiệu lực trong kỳ này.")
    values = {key: parse_integer(data.get(key, ""), label, required=True) for key, label in (
        ("rent_price", "Tiền phòng"), ("water_price", "Giá nước"), ("service_price", "Dịch vụ"), ("electricity_price", "Đơn giá điện"))}
    values["people_count"] = parse_integer(data.get("people_count", ""), "Số người tính nước", 1, 31, True)
    payment_day = parse_integer(data.get("payment_day", ""), "Ngày đến hạn", 1, 31, True)
    year, month = map(int, period.split("-"))
    values.update(room_id=room.id, tenancy_id=tenant.id, period=period, room_code=room.code, tenant_name=tenant.tenant_name,
                  start_value=reading.start_value, end_value=reading.end_value, created_by=user_id,
                  due_date=date(year, month, min(payment_day, calendar.monthrange(year, month)[1])))
    bill = MonthlyBill(**values)
    if save:
        db.session.add(bill)
        db.session.commit()
    return bill
