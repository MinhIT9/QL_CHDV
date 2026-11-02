from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.extensions import db
from app.models import Room, Tenancy
from app.services.rooms import save_room
from app.services.electricity import current_period, valid_period

bp = Blueprint("rooms", __name__)


def room_query():
    return db.select(Room).options(
        selectinload(Room.tenancies).selectinload(Tenancy.occupants),
        selectinload(Room.tenancies).selectinload(Tenancy.vehicles),
        selectinload(Room.readings),
    ).order_by(Room.code)


@bp.get("/")
@login_required
def index():
    period = request.args.get("period", current_period())
    if not valid_period(period):
        period = current_period()
    rooms = db.session.scalars(room_query()).all()
    q = request.args.get("q", "").strip().lower()
    if q:
        rooms = [r for r in rooms if q in r.code.lower() or (r.current_tenancy and q in r.current_tenancy.tenant_name.lower())]
    readings = {r.id: next((item for item in r.readings if item.period == period), None) for r in rooms}
    return render_template("rooms/index.html", rooms=rooms, period=period, readings=readings, q=q,
                           total_consumption=sum(item.consumption for item in readings.values() if item))


@bp.route("/rooms/new", methods=["GET", "POST"])
@bp.route("/rooms/<int:room_id>/edit", methods=["GET", "POST"])
@login_required
def edit(room_id=None):
    room = db.get_or_404(Room, room_id) if room_id else None
    if request.method == "POST":
        try:
            saved = save_room(room, request.form)
            db.session.commit()
        except (ValueError, IntegrityError) as error:
            db.session.rollback()
            flash(str(error) if isinstance(error, ValueError) else "Mã phòng đã tồn tại hoặc dữ liệu vừa được thay đổi. Vui lòng kiểm tra lại.", "danger")
            return render_template("rooms/form.html", room=room, values=request.form), 400
        flash("Đã lưu thông tin phòng.", "success")
        return redirect(url_for("rooms.detail", room_id=saved.id))
    current = room.current_tenancy if room else None
    values = {
        "code": room.code if room else "",
        "status": ("inactive" if not room.active else "occupied" if current else "vacant") if room else "vacant",
        "tenant_name": current.tenant_name if current else "",
        "occupants": "\n".join(item.name for item in current.occupants) if current else "",
        "vehicles": "\n".join(item.plate for item in current.vehicles) if current else "",
        "note": room.note if room else "",
    }
    return render_template("rooms/form.html", room=room, values=values)


@bp.get("/rooms/<int:room_id>")
@login_required
def detail(room_id):
    return render_template("rooms/detail.html", room=db.get_or_404(Room, room_id))


@bp.post("/rooms/<int:room_id>/remove")
@login_required
def remove(room_id):
    room = db.get_or_404(Room, room_id)
    try:
        if room.readings or room.tenancies:
            room.active = False
            if room.current_tenancy:
                from app.models import utcnow
                room.current_tenancy.ended_at = utcnow()
            flash("Đã ngừng sử dụng phòng và giữ nguyên lịch sử.", "success")
        else:
            db.session.delete(room)
            flash("Đã xóa phòng chưa có lịch sử.", "success")
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Phòng vừa có dữ liệu liên quan. Hãy tải lại và ngừng sử dụng phòng.", "danger")
    return redirect(url_for("rooms.index"))
