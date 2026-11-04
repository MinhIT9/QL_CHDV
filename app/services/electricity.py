import re
from datetime import datetime, timedelta, timezone

from app.extensions import db
from app.models import ElectricityReading, Room
from app.services.photos import stage_photo, upload_batch

MAX_READING = 2_147_483_647


def reading_cost(reading, bill=None, fallback_price=None):
    """Prefer bill/saved prices; current-rate estimates must be explicit."""
    price = bill.electricity_price if bill else reading.electricity_price if reading else None
    current_price = price is None
    if current_price:
        price = fallback_price
    return {
        "price": price,
        "amount": reading.consumption * price if reading and price is not None else None,
        "estimated": bill is None,
        "current_price": current_price,
    }


def current_period():
    return datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m")


def valid_period(value):
    return bool(re.fullmatch(r"[12]\d{3}-(0[1-9]|1[0-2])", value or ""))


def previous_period(period):
    year, month = map(int, period.split("-"))
    return f"{year - 1}-12" if month == 1 else f"{year}-{month - 1:02d}"


def reading_context(room, period):
    existing = next((item for item in room.readings if item.period == period), None)
    prior = [item for item in room.readings if item.period < period]
    later = [item for item in room.readings if item.period > period]
    latest = max(prior, key=lambda item: item.period) if prior else None
    error = None
    if not existing and later:
        error = "Đã có kỳ sau. V1 không cho chèn ngược lịch sử."
    elif not existing and latest and latest.period != previous_period(period):
        error = f"Cần chốt kỳ {previous_period(period)} trước (kỳ gần nhất: {latest.period})."
    return {"room": room, "existing": existing, "start": latest.end_value if latest else None, "error": error}


def integer_reading(value, label):
    if not re.fullmatch(r"\d{1,10}", value or ""):
        raise ValueError(f"{label} phải là số nguyên không âm.")
    result = int(value)
    if result > MAX_READING:
        raise ValueError(f"{label} quá lớn.")
    return result


def save_readings(period, data, user_id, files):
    if not valid_period(period) or period > current_period():
        raise ValueError("Kỳ chốt không hợp lệ hoặc nằm trong tương lai.")
    # Serialize SQLite writers before re-reading history to avoid stale concurrent starts.
    if db.engine.dialect.name == "sqlite":
        db.session.execute(db.text("BEGIN IMMEDIATE"))
    rooms = db.session.scalars(db.select(Room).where(Room.active.is_(True)).order_by(Room.code)).all()
    submitted = []
    for room in rooms:
        raw = data.get(f"end_{room.id}", "").strip()
        if not raw:
            continue
        context = reading_context(room, period)
        if context["existing"]:
            raise ValueError(f"Phòng {room.code} đã chốt kỳ này. Không ghi đè lịch sử.")
        if context["error"]:
            raise ValueError(f"Phòng {room.code}: {context['error']}")
        start = context["start"]
        if start is None:
            start = integer_reading(data.get(f"start_{room.id}", "").strip(), f"Đầu kỳ phòng {room.code}")
        end = integer_reading(raw, f"Cuối kỳ phòng {room.code}")
        if end < start:
            raise ValueError(f"Phòng {room.code}: cuối kỳ không được nhỏ hơn đầu kỳ. V1 chưa hỗ trợ thay đồng hồ.")
        tenant = room.current_tenancy
        submitted.append(ElectricityReading(room_id=room.id, period=period, start_value=start, end_value=end,
                                           electricity_price=tenant.electricity_price if tenant else None, created_by=user_id))
    if not submitted:
        raise ValueError("Hãy nhập chỉ số cuối cho ít nhất một phòng chưa chốt.")
    with upload_batch() as staged:
        for reading in submitted:
            upload = files.get(f"photo_{reading.room_id}")
            if upload and upload.filename:
                stage_photo(upload, user_id, staged, reading=reading)
        db.session.add_all(submitted)
        db.session.commit()
    return len(submitted)
