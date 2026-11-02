from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError, OperationalError

from app.extensions import db
from app.models import Room
from app.rooms.routes import room_query
from app.services.electricity import current_period, reading_context, save_readings, valid_period

bp = Blueprint("electricity", __name__, url_prefix="/electricity")


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    period = request.form.get("period", current_period()) if request.method == "POST" else request.args.get("period", current_period())
    if not valid_period(period):
        flash("Kỳ tháng không hợp lệ.", "danger")
        return redirect(url_for("electricity.index"))
    status = 200
    if request.method == "POST":
        try:
            count = save_readings(period, request.form, current_user.id)
        except (ValueError, IntegrityError, OperationalError) as error:
            db.session.rollback()
            flash(str(error) if isinstance(error, ValueError) else "Dữ liệu vừa được cập nhật hoặc đang bận. Hãy tải lại trước khi lưu.", "danger")
            status = 400
        else:
            flash(f"Đã chốt điện cho {count} phòng, kỳ {period}.", "success")
            return redirect(url_for("electricity.index", period=period))
    rooms = db.session.scalars(room_query().where(Room.active.is_(True))).all()
    contexts = [reading_context(room, period) for room in rooms]
    return render_template("electricity/index.html", contexts=contexts, period=period,
                           done=sum(bool(item["existing"]) for item in contexts),
                           values=request.form if request.method == "POST" else {}), status
