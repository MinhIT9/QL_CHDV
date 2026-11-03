from flask import Blueprint, abort, flash, redirect, request, send_file, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import ElectricityReading, Photo, Tenancy
from app.services.photos import photo_path, stage_photo, upload_batch

bp = Blueprint("photos", __name__, url_prefix="/photos")


@bp.get("/<int:photo_id>")
@login_required
def view(photo_id):
    photo = db.get_or_404(Photo, photo_id)
    if photo.status != "ready":
        abort(404)
    path = photo_path(photo)
    if not path.is_file():
        abort(404)
    return send_file(path, mimetype="image/webp", max_age=0)


@bp.post("/<kind>/<int:owner_id>")
@login_required
def add(kind, owner_id):
    if kind not in {"contract", "electricity"}:
        abort(404)
    owner = db.get_or_404(Tenancy if kind == "contract" else ElectricityReading, owner_id)
    try:
        with upload_batch() as staged:
            stage_photo(request.files.get("photo"), current_user.id, staged,
                        tenancy=owner if kind == "contract" else None,
                        reading=owner if kind == "electricity" else None)
            db.session.commit()
    except (ValueError, OSError, SQLAlchemyError) as error:
        flash(str(error) if isinstance(error, ValueError) else "Không thể lưu ảnh. Hãy thử lại.", "danger")
    else:
        flash("Đã nhận ảnh, đang xử lý. Tải lại trang sau vài giây để xem.", "success")
    if kind == "electricity":
        return redirect(url_for("billing.correct", reading_id=owner.id, _anchor="meter-photos"))
    return redirect(url_for("rooms.detail", room_id=owner.room_id))
