import re

from flask import Blueprint, abort, flash, jsonify, redirect, request, send_file, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import ElectricityReading, Photo, Tenancy
from app.services.photos import photo_path, stage_photo, upload_batch

bp = Blueprint("photos", __name__, url_prefix="/photos")


def photo_state(photo):
    return {"id": photo.id, "status": photo.status,
            "url": url_for("photos.view", photo_id=photo.id, v=photo.display_token) if photo.display_token else None}


@bp.get("/status")
@login_required
def status():
    values = request.args.get("ids", "").split(",")
    if len(values) > 100 or not all(value.isascii() and value.isdigit() and len(value) <= 10 for value in values):
        abort(400)
    return jsonify(photos=[photo_state(photo) for photo in db.session.scalars(db.select(Photo).where(Photo.id.in_([int(v) for v in values])))])


@bp.get("/<int:photo_id>")
@login_required
def view(photo_id):
    photo = db.get_or_404(Photo, photo_id)
    if not photo.display_token:
        abort(404)
    path = photo_path(photo).with_name(f"{photo.display_token}.webp")
    if not path.is_file():
        abort(404)
    return send_file(path, mimetype="image/webp", max_age=0)


@bp.post("/<kind>/<int:owner_id>")
@login_required
def add(kind, owner_id):
    if kind not in {"contract", "electricity"}:
        abort(404)
    owner = db.get_or_404(Tenancy if kind == "contract" else ElectricityReading, owner_id)
    ajax = request.headers.get("X-Photo-Upload") == "1"
    token = request.form.get("upload_token", "")
    if db.engine.dialect.name == "sqlite":
        db.session.execute(db.text("BEGIN IMMEDIATE"))
    if ajax:
        if not re.fullmatch(r"[a-f0-9]{32}", token):
            return jsonify(error="Mã tải ảnh không hợp lệ."), 400
        existing = db.session.scalar(db.select(Photo).where(Photo.token == token))
        if existing:
            if existing.created_by != current_user.id or (existing.reading_id if kind == "electricity" else existing.tenancy_id) != owner.id or (kind == "electricity") != (existing.reading_id is not None):
                abort(409)
            return jsonify(photo=photo_state(existing))
    try:
        with upload_batch() as staged:
            photo = stage_photo(
                request.files.get("photo"), current_user.id, staged,
                tenancy=owner if kind == "contract" else None,
                reading=owner if kind == "electricity" else None,
                token=token if ajax else None,
            )
            db.session.commit()
    except (ValueError, OSError, SQLAlchemyError) as error:
        if ajax:
            return jsonify(error=str(error) if isinstance(error, ValueError) else "Không thể lưu ảnh. Hãy thử lại."), 400
        flash(str(error) if isinstance(error, ValueError) else "Không thể lưu ảnh. Hãy thử lại.", "danger")
    else:
        if ajax:
            return jsonify(photo=photo_state(photo))
        flash("Đã nhận ảnh, đang xử lý. Tải lại trang sau vài giây để xem.", "success")
    if kind == "electricity":
        return redirect(url_for("billing.correct", reading_id=owner.id, _anchor="meter-photos"))
    return redirect(url_for("rooms.detail", room_id=owner.room_id))
