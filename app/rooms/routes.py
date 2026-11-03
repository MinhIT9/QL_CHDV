from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.exc import StaleDataError

from app.extensions import db
from app.models import Room, Tenancy
from app.services.rooms import save_room
from app.services.electricity import current_period, valid_period
from app.services.contracts import check_version, due_date, end_tenancy, local_today, renewal_preview, renew_contract

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
                           total_consumption=sum(item.consumption for item in readings.values() if item),
                           due_dates={r.id: due_date(r.current_tenancy, period) if r.current_tenancy else None for r in rooms}, today=local_today())


@bp.route("/rooms/new", methods=["GET", "POST"])
@bp.route("/rooms/<int:room_id>/edit", methods=["GET", "POST"])
@login_required
def edit(room_id=None):
    room = db.get_or_404(Room, room_id) if room_id else None
    if request.method == "POST":
        try:
            saved = save_room(room, request.form)
            db.session.commit()
        except (ValueError, IntegrityError, StaleDataError, OperationalError) as error:
            db.session.rollback()
            flash(str(error) if isinstance(error, ValueError) else "Mã phòng đã tồn tại hoặc dữ liệu vừa được thay đổi. Vui lòng kiểm tra lại.", "danger")
            return render_template("rooms/form.html", room=room, values=request.form, today=local_today()), 400
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
        "tenancy_id": str(current.id) if current else "",
        "tenancy_version": str(current.version) if current else "",
    }
    for key in ("contract_start", "contract_end", "rent_price", "electricity_price", "water_price", "service_price", "deposit_amount", "payment_day"):
        value = getattr(current, key) if current else None
        values[key] = value.isoformat() if hasattr(value, "isoformat") else value if value is not None else ""
    return render_template("rooms/form.html", room=room, values=values, today=local_today())


@bp.get("/rooms/<int:room_id>")
@login_required
def detail(room_id):
    room = db.get_or_404(Room, room_id)
    period = request.args.get("period", current_period())
    if not valid_period(period):
        period = current_period()
    return render_template("rooms/detail.html", room=room, today=local_today(), period=period,
                           payment_due=due_date(room.current_tenancy, period) if room.current_tenancy else None)


@bp.route("/rooms/<int:room_id>/remove", methods=["GET", "POST"])
@login_required
def remove(room_id):
    room = db.get_or_404(Room, room_id)
    if request.method == "GET":
        return render_template("rooms/remove.html", room=room, today=local_today())
    try:
        if room.current_tenancy:
            check_version(room.current_tenancy, request.form)
            end_tenancy(room.current_tenancy, request.form.get("move_out_date", ""))
        elif request.form.get("tenancy_id"):
            raise ValueError("Đợt thuê đã thay đổi. Hãy tải lại trang.")
        if room.readings or room.tenancies:
            room.active = False
            flash("Đã ngừng sử dụng phòng và giữ nguyên lịch sử.", "success")
        else:
            db.session.delete(room)
            flash("Đã xóa phòng chưa có lịch sử.", "success")
        db.session.commit()
    except (ValueError, IntegrityError, StaleDataError, OperationalError) as error:
        db.session.rollback()
        flash(str(error) if isinstance(error, ValueError) else "Dữ liệu vừa thay đổi. Hãy tải lại trước khi ngừng sử dụng phòng.", "danger")
        return render_template("rooms/remove.html", room=room, today=local_today()), 400
    return redirect(url_for("rooms.index"))


@bp.route("/rooms/<int:room_id>/renew", methods=["GET", "POST"])
@login_required
def renew(room_id):
    room = db.get_or_404(Room, room_id)
    tenant = room.current_tenancy
    if tenant is None:
        flash("Phòng không có đợt thuê hiện tại để gia hạn.", "warning")
        return redirect(url_for("rooms.detail", room_id=room.id))
    preview = None
    values = request.form if request.method == "POST" else {"tenancy_id": str(tenant.id), "tenancy_version": str(tenant.version), "months": "1"}
    if request.method == "POST":
        try:
            if request.form.get("action") == "confirm":
                result = renew_contract(tenant, request.form, current_user.id)
                flash(f"Đã gia hạn {result['months']} tháng, đến {result['new_end'].strftime('%d/%m/%Y')}.", "success")
                return redirect(url_for("rooms.detail", room_id=room.id))
            preview = renewal_preview(tenant, request.form)
        except (ValueError, IntegrityError, StaleDataError, OperationalError) as error:
            db.session.rollback()
            flash(str(error) if isinstance(error, ValueError) else "Hợp đồng vừa thay đổi. Hãy tải lại trang và xem trước lại.", "danger")
            return render_template("rooms/renew.html", room=room, tenant=tenant, values=values, preview=None, today=local_today()), 400
    return render_template("rooms/renew.html", room=room, tenant=tenant, values=values, preview=preview, today=local_today())
