from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError, OperationalError

from app.auth.routes import root_required
from app.extensions import db
from app.models import ElectricityReading, MonthlyBill, ReadingRevision, Receipt, Room, utcnow
from app.services.contracts import local_today, parse_date
from sqlalchemy.orm import selectinload
from app.services.billing import bill_tenancy, bill_values, correction, lock_writes, reading_pair, reading_stamp
from app.services.electricity import current_period, valid_period

bp = Blueprint("billing", __name__)
WRITE_ERRORS = (ValueError, IntegrityError, OperationalError, OSError)


def report(error):
    db.session.rollback()
    flash(str(error) if isinstance(error, ValueError) else "Dữ liệu vừa thay đổi hoặc đang bận. Hãy tải lại trang.", "danger")


@bp.route("/electricity/<int:reading_id>/correct", methods=["GET", "POST"])
@login_required
def correct(reading_id):
    reading = db.get_or_404(ElectricityReading, reading_id)
    values = request.form if request.method == "POST" else {"start_value": reading.start_value, "end_value": reading.end_value, "stamp": reading_stamp(reading)}
    preview, status = None, 200
    if request.method == "POST":
        try:
            preview = correction(reading, request.form, current_user.id, request.form.get("action") == "confirm", request.files.get("photo"))
            if request.form.get("action") == "confirm":
                flash("Đã điều chỉnh số điện và lưu lịch sử các kỳ bị ảnh hưởng.", "success")
                return redirect(url_for("billing.correct", reading_id=reading.id))
        except WRITE_ERRORS as error:
            report(error)
            status = 400
    revisions = db.session.scalars(db.select(ReadingRevision).where(ReadingRevision.reading_id == reading.id).order_by(ReadingRevision.id.desc())).all()
    return render_template("electricity/correct.html", reading=reading, values=values, preview=preview, revisions=revisions, previous=reading_pair(reading)[0]), status


@bp.get("/bills")
@login_required
def index():
    period = request.args.get("period", current_period())
    if not valid_period(period):
        period = current_period()
    bills = db.session.scalars(db.select(MonthlyBill).options(selectinload(MonthlyBill.receipts)).where(MonthlyBill.period == period)).all()
    today = local_today()
    bills.sort(key=lambda b: (3 if b.cancelled_at else 2 if b.paid_receipt else 0 if b.due_date < today else 1, b.room_code, b.id))
    return render_template("billing/index.html", period=period, bills=bills, rooms=db.session.scalars(db.select(Room).order_by(Room.code)).all(), today=today)


@bp.route("/rooms/<int:room_id>/bill", methods=["GET", "POST"])
@login_required
def create(room_id):
    room = db.get_or_404(Room, room_id)
    period = request.form.get("period", "") if request.method == "POST" else request.args.get("period", current_period())
    preview, values = None, request.form
    try:
        tenant = bill_tenancy(room, period)
        if request.method == "POST":
            preview = bill_values(room, period, values, current_user.id, values.get("action") == "confirm")
            if values.get("action") == "confirm":
                flash("Đã chốt tiền. Giá và số người của phiếu được giữ cố định.", "success")
                return redirect(url_for("billing.index", period=period))
        else:
            reading = db.session.scalar(db.select(ElectricityReading).where(ElectricityReading.room_id == room.id, ElectricityReading.period == period))
            if not reading:
                raise ValueError("Cần lưu số điện kỳ này trước khi tính tiền.")
            values = {key: getattr(tenant, key) if getattr(tenant, key) is not None else "" for key in ("rent_price", "electricity_price", "water_price", "service_price", "payment_day")}
            values.update(period=period, people_count=tenant.people_count, tenancy_id=tenant.id, tenancy_version=tenant.version, stamp=reading_stamp(reading))
    except WRITE_ERRORS as error:
        report(error)
        if request.method == "GET":
            return redirect(url_for("billing.index", period=period if valid_period(period) else current_period()))
        return render_template("billing/form.html", room=room, values=values, preview=None, period=period), 400
    return render_template("billing/form.html", room=room, values=values, preview=preview, period=period)


@bp.post("/bills/<int:bill_id>/cancel")
@root_required
def cancel(bill_id):
    try:
        lock_writes()
        bill = db.get_or_404(MonthlyBill, bill_id)
        reason = request.form.get("reason", "").strip()
        if bill.cancelled_at or not reason or len(reason) > 500:
            raise ValueError("Phiếu đã hủy hoặc thiếu lý do hợp lệ (tối đa 500 ký tự).")
        if bill.paid_receipt:
            raise ValueError("Phiếu đã thu tiền. Root cần hoàn tác ghi nhận thu có lý do trước khi hủy phiếu.")
        bill.cancelled_at, bill.cancelled_by, bill.cancel_reason = utcnow(), current_user.id, reason
        db.session.commit()
        flash("Đã hủy hiệu lực phiếu và giữ nguyên bản cũ. Có thể sửa điện rồi lập phiếu mới.", "success")
    except WRITE_ERRORS as error:
        report(error)
    return redirect(url_for("billing.index", period=db.get_or_404(MonthlyBill, bill_id).period))


@bp.post("/bills/<int:bill_id>/receive")
@login_required
def receive(bill_id):
    try:
        lock_writes()
        bill = db.get_or_404(MonthlyBill, bill_id)
        paid_date = parse_date(request.form.get("paid_date", ""), "Ngày thu", required=True)
        note = request.form.get("note", "").strip()
        if bill.cancelled_at or bill.paid_receipt:
            raise ValueError("Phiếu đã hủy hoặc đã được ghi nhận thu đủ.")
        if request.form.get("receipt_version") != str(bill.receipts[-1].id if bill.receipts else 0):
            raise ValueError("Lịch sử thu đã thay đổi. Hãy tải lại trang trước khi xác nhận.")
        if paid_date > local_today() or len(note) > 500:
            raise ValueError("Ngày thu không được trong tương lai; ghi chú tối đa 500 ký tự.")
        db.session.add(Receipt(bill=bill, amount=bill.total, paid_date=paid_date, note=note, created_by=current_user.id))
        db.session.commit()
        flash("Đã ghi nhận thu đủ. Phiếu được chuyển xuống nhóm Đã thu.", "success")
    except WRITE_ERRORS as error:
        report(error)
    return redirect(url_for("billing.index", period=db.get_or_404(MonthlyBill, bill_id).period))


@bp.post("/receipts/<int:receipt_id>/reverse")
@root_required
def reverse_receipt(receipt_id):
    try:
        lock_writes()
        receipt = db.get_or_404(Receipt, receipt_id)
        reason = request.form.get("reason", "").strip()
        if receipt.reversed_at or not reason or len(reason) > 500:
            raise ValueError("Ghi nhận đã hoàn tác hoặc thiếu lý do hợp lệ (tối đa 500 ký tự).")
        receipt.reversed_at, receipt.reversed_by, receipt.reverse_reason = utcnow(), current_user.id, reason
        db.session.commit()
        flash("Đã hoàn tác ghi nhận thu và giữ lịch sử. Đây không phải thao tác hoàn tiền thực tế.", "success")
    except WRITE_ERRORS as error:
        report(error)
    return redirect(url_for("billing.index", period=db.get_or_404(Receipt, receipt_id).bill.period))
