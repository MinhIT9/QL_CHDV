from app.extensions import db
from app.models import Occupant, Room, Tenancy, Vehicle
from app.services.contracts import check_version, contract_values, end_tenancy


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

    current = room.current_tenancy if room else None
    if current:
        check_version(current, data)
    elif data.get("tenancy_id"):
        raise ValueError("Đợt thuê đã kết thúc. Hãy tải lại trang.")
    new_tenancy = data.get("new_tenancy") == "on"
    terms = contract_values(data, None if new_tenancy else current) if status == "occupied" else None
    if current and (status != "occupied" or new_tenancy):
        end_tenancy(current, data.get("move_out_date", ""))
    if terms and room and (current is None or new_tenancy):
        past_dates = [item.move_out_date for item in room.tenancies if item.move_out_date]
        if past_dates and terms["contract_start"] < max(past_dates):
            raise ValueError("Ngày bắt đầu hợp đồng mới không được trước ngày khách cũ trả phòng.")
    if room is None:
        room = Room()
        db.session.add(room)
    room.code, room.note, room.active = code, note, status != "inactive"
    if current and (status != "occupied" or new_tenancy):
        # End the old tenancy before creating the next one (unique active tenancy).
        db.session.flush()
        current = None
    if status == "occupied":
        if current is None:
            current = Tenancy(room=room, tenant_name=tenant_name)
            db.session.add(current)
        current.tenant_name = tenant_name
        if current.id is not None:
            current.version += 1
        for key, value in terms.items():
            if key == "contract_end" and value != current.contract_end:
                current.contract_anchor_day = value.day if value else None
            setattr(current, key, value)
        # Retained legacy DB column; never a separate editable business date.
        current.move_in_date = current.contract_start
        current.occupants = [Occupant(name=name) for name in people]
        current.vehicles = [Vehicle(plate=plate) for plate in plates]
    return room
