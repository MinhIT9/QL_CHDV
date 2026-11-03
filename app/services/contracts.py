import calendar
import re
from datetime import date, datetime, timedelta, timezone

from app.extensions import db
from app.models import ContractRenewal, utcnow


def local_today():
    return datetime.now(timezone(timedelta(hours=7))).date()


def parse_date(value, label, required=False):
    if not value:
        if required:
            raise ValueError(f"{label} là bắt buộc.")
        return None
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{label} không hợp lệ.") from None


def parse_integer(value, label, minimum=0, maximum=2147483647, required=False):
    if value == "":
        if required:
            raise ValueError(f"{label} là bắt buộc; nhập 0 nếu miễn phí.")
        return None
    if not re.fullmatch(r"[0-9]{1,10}", value) or not minimum <= int(value) <= maximum:
        raise ValueError(f"{label} phải là số nguyên từ {minimum} đến {maximum}.")
    return int(value)


def contract_values(data, current=None):
    result = {}
    for key, label in (("contract_start", "Ngày bắt đầu hợp đồng"), ("contract_end", "Ngày hết hạn hợp đồng")):
        required = current is None or getattr(current, key) is not None
        result[key] = parse_date(data.get(key, "").strip(), label, required)
    for key, label in (("electricity_price", "Giá điện"), ("rent_price", "Tiền phòng"), ("water_price", "Giá nước"), ("service_price", "Phí dịch vụ"), ("deposit_amount", "Tiền cọc"), ("payment_day", "Ngày đóng tiền")):
        required = current is None or getattr(current, key) is not None
        result[key] = parse_integer(data.get(key, "").strip(), label, 1 if key == "payment_day" else 0, 31 if key == "payment_day" else 2147483647, required)
    start, end = result["contract_start"], result["contract_end"]
    if bool(start) != bool(end) or (start and end < start):
        raise ValueError("Cần nhập đủ ngày bắt đầu/hết hạn; hết hạn không được trước ngày bắt đầu.")
    if start and start > local_today():
        raise ValueError("Ngày bắt đầu hợp đồng không được trong tương lai. V1 chưa nhận đặt trước.")
    if current and current.renewals and (start != current.contract_start or end != current.contract_end):
        raise ValueError("Hợp đồng đã gia hạn: không sửa trực tiếp ngày bắt đầu/hết hạn. Hãy dùng chức năng gia hạn.")
    return result


def check_version(current, data):
    if str(current.id) != data.get("tenancy_id") or str(current.version) != data.get("tenancy_version"):
        raise ValueError("Đợt thuê đã thay đổi hoặc biểu mẫu đã cũ. Hãy tải lại trang trước khi lưu.")


def end_tenancy(current, raw_date):
    move_out = parse_date(raw_date, "Ngày trả phòng thực tế", required=True)
    if move_out > local_today() or (current.contract_start and move_out < current.contract_start):
        raise ValueError("Ngày trả phòng phải từ ngày bắt đầu hợp đồng đến hôm nay.")
    current.move_out_date = move_out
    current.move_in_date = current.contract_start
    current.ended_at = utcnow()


def add_months(value, months, anchor_day):
    index = value.year * 12 + value.month - 1 + months
    year, month_index = divmod(index, 12)
    if year > 9999:
        raise ValueError("Ngày gia hạn vượt giới hạn năm 9999.")
    month = month_index + 1
    return date(year, month, min(anchor_day, calendar.monthrange(year, month)[1]))


def due_date(tenancy, period):
    if tenancy.payment_day is None:
        return None
    year, month = map(int, period.split("-"))
    return date(year, month, min(tenancy.payment_day, calendar.monthrange(year, month)[1]))


def renewal_preview(current, data):
    if current is None or current.ended_at is not None:
        raise ValueError("Chỉ gia hạn đợt thuê hiện tại chưa trả phòng.")
    check_version(current, data)
    if current.contract_start is None or current.contract_end is None:
        raise ValueError("Cần bổ sung ngày hợp đồng trước khi gia hạn.")
    months = parse_integer(data.get("months", ""), "Số tháng gia hạn", 1, 120, True)
    note = data.get("note", "").strip()
    if len(note) > 1000:
        raise ValueError("Ghi chú gia hạn tối đa 1.000 ký tự.")
    return {"old_end": current.contract_end, "new_end": add_months(current.contract_end, months, current.contract_anchor_day or current.contract_end.day), "months": months, "note": note, "overdue": current.contract_end < local_today()}


def renew_contract(current, data, user_id):
    preview = renewal_preview(current, data)
    if data.get("expected_new_end") != preview["new_end"].isoformat():
        raise ValueError("Hạn mới chưa được xem trước hoặc đã thay đổi. Hãy xem trước lại.")
    if preview["overdue"] and data.get("confirm_overdue") != "on":
        raise ValueError("Hợp đồng đã quá hạn: cần xác nhận gia hạn từ hạn cũ.")
    current.contract_anchor_day = current.contract_anchor_day or current.contract_end.day
    current.contract_end = preview["new_end"]
    db.session.add(ContractRenewal(tenancy=current, old_end=preview["old_end"], new_end=preview["new_end"], months=preview["months"], note=preview["note"], created_by=user_id))
    db.session.commit()
    return preview
