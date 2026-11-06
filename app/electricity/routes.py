from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError, OperationalError

from app.extensions import db
from app.models import ElectricityReading, MonthlyBill, Photo, ReadingRevision, Room
from app.services.queries import active_bill_query, room_query
from app.services.electricity import current_period, reading_context, reading_cost, save_readings, valid_period

bp = Blueprint("electricity", __name__, url_prefix="/electricity")


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    period = request.form.get("period", current_period()) if request.method == "POST" else request.args.get("period", current_period())
    if not valid_period(period):
        flash("Kỳ tháng không hợp lệ.", "danger")
        return redirect(url_for("electricity.index"))
    status = 200
    ajax = request.headers.get("X-Meter-Save") == "1"
    if request.method == "POST":
        try:
            count = save_readings(period, request.form, current_user.id, request.files)
        except (ValueError, IntegrityError, OperationalError, OSError) as error:
            db.session.rollback()
            if ajax:
                return jsonify(error=str(error) if isinstance(error, ValueError) else "Dữ liệu vừa thay đổi. Hãy kiểm tra lại trước khi lưu."), 400
            flash(str(error) if isinstance(error, ValueError) else "Dữ liệu vừa được cập nhật hoặc đang bận. Hãy tải lại trước khi lưu.", "danger")
            status = 400
        else:
            if not ajax:
                flash(f"Đã chốt điện cho {count} phòng, kỳ {period}.", "success")
                return redirect(url_for("electricity.index", period=period))
    rooms = db.session.scalars(room_query().where(Room.active.is_(True))).all()
    contexts = [reading_context(room, period) for room in rooms]
    contexts.sort(key=lambda row: row["existing"] is not None)
    draft_photos = {photo.room_id: photo for photo in db.session.scalars(db.select(Photo).where(Photo.period == period, Photo.room_id.is_not(None)))}
    bills = {bill.room_id: bill for bill in db.session.scalars(active_bill_query().where(MonthlyBill.period == period))}
    updated = dict(db.session.execute(db.select(ReadingRevision.reading_id, db.func.max(ReadingRevision.created_at)).join(ElectricityReading, ReadingRevision.reading_id == ElectricityReading.id).where(ElectricityReading.period == period).group_by(ReadingRevision.reading_id)).all())
    for row in contexts:
        reading, tenant = row["existing"], row["room"].current_tenancy
        bill = bills.get(row["room"].id)
        row.update(reading_cost(reading, bill, tenant.electricity_price if tenant else None))
        row["updated_at"] = updated.get(reading.id) if reading else None
        row["photo_locked"] = bill is not None
        row["meter_photos"] = reading.photos if reading else [draft_photos[row["room"].id]] if row["room"].id in draft_photos else []
    html = render_template("electricity/index.html", contexts=contexts, period=period,
                           done=sum(bool(item["existing"]) for item in contexts),
                           values=request.form if request.method == "POST" else {})
    return jsonify(html=html) if ajax else (html, status)
