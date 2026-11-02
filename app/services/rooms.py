from app.extensions import db
from app.models import Occupant, Room, Tenancy, Vehicle, utcnow


def lines(value, max_length, label):
    values = [line.strip() for line in value.splitlines() if line.strip()]
    if len(values) > 30 or any(len(item) > max_length for item in values):
        raise ValueError(f"{label}: tối đa 30 dòng, mỗi dòng tối đa {max_length} ký tự.")
    return list(dict.fromkeys(values))


def save_room(room, data):
    code = data.get("code", "").strip().upper()
    status = data.get("status", "vacant")
    tenant_name = data.get("tenant_name", "").strip()
    note = data.get("note", "").strip()
    people = lines(data.get("occupants", ""), 120, "Người ở cùng")
    plates = lines(data.get("vehicles", "").upper(), 30, "Biển số xe")
    if not code or len(code) > 30:
        raise ValueError("Mã phòng bắt buộc và tối đa 30 ký tự.")
    if status not in {"vacant", "occupied", "inactive"}:
        raise ValueError("Trạng thái phòng không hợp lệ.")
    if len(note) > 2000 or len(tenant_name) > 120:
        raise ValueError("Ghi chú tối đa 2.000 ký tự; tên khách tối đa 120 ký tự.")
    if status == "occupied" and not tenant_name:
        raise ValueError("Phòng đang thuê cần có tên khách thuê chính.")
    if status != "occupied" and (tenant_name or people or plates):
        raise ValueError("Phòng trống/ngừng sử dụng không nhận thông tin khách mới. Xóa các ô khách hoặc chọn Đang thuê.")

    if room is None:
        room = Room()
        db.session.add(room)
    room.code, room.note, room.active = code, note, status != "inactive"
    current = room.current_tenancy
    new_tenancy = data.get("new_tenancy") == "on"
    if current and (status != "occupied" or new_tenancy):
        current.ended_at = utcnow()
        # End the old tenancy before creating the next one (unique active tenancy).
        db.session.flush()
        current = None
    if status == "occupied":
        if current is None:
            current = Tenancy(room=room, tenant_name=tenant_name)
            db.session.add(current)
        current.tenant_name = tenant_name
        current.occupants = [Occupant(name=name) for name in people]
        current.vehicles = [Vehicle(plate=plate) for plate in plates]
    return room
