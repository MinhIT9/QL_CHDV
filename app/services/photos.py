"""Private uploads and a durable queue processed by one CLI worker."""
import os
import time
import uuid
import warnings
from contextlib import contextmanager
from pathlib import Path

import click
from flask import current_app
from PIL import Image, ImageOps, UnidentifiedImageError

from app.extensions import db
from app.models import MonthlyBill, Photo, utcnow

FORMATS = ("JPEG", "PNG", "WEBP")
MAX_PIXELS = 24_000_000


def photo_root():
    root = Path(current_app.config["PHOTO_ROOT"])
    for name in ("tmp", "contracts", "electricity"):
        (root / name).mkdir(parents=True, exist_ok=True, mode=0o700)
    return root


def photo_path(photo, temporary=False):
    root = photo_root()
    if temporary:
        return root / "tmp" / f"{photo.token}.upload"
    folder = "contracts" if photo.tenancy_id else "electricity"
    return root / folder / f"{photo.token}.webp"


def meter_photo_locked(reading):
    return db.session.scalar(db.select(MonthlyBill.id).where(
        MonthlyBill.room_id == reading.room_id,
        MonthlyBill.period == reading.period,
        MonthlyBill.cancelled_at.is_(None),
    )) is not None


@contextmanager
def upload_batch():
    """Remove staged originals if the business transaction does not commit."""
    staged = []
    try:
        yield staged
    except BaseException:
        db.session.rollback()
        for photo in staged:
            photo_path(photo, temporary=True).unlink(missing_ok=True)
        raise


def attach_meter_photo(reading):
    """Move the room/month image to its real reading in the same transaction."""
    photo = db.session.scalar(db.select(Photo).where(
        Photo.room_id == reading.room_id, Photo.period == reading.period))
    if photo:
        photo.room_id, photo.period = None, None
        photo.reading = reading


def stage_photo(upload, user_id, staged, *, tenancy=None, reading=None, room=None, period=None, token=None):
    if upload is None or not upload.filename:
        raise ValueError("Cần chọn ảnh chốt số điện.")
    existing = None
    if reading and reading.id is not None:
        if meter_photo_locked(reading):
            raise ValueError("Phiếu tiền kỳ này còn hiệu lực. Hãy hủy phiếu chưa thu trước khi sửa ảnh công tơ; phiếu đã thu cần root xử lý.")
        existing = db.session.scalar(db.select(Photo).where(Photo.reading_id == reading.id))
    elif room:
        if db.session.scalar(db.select(MonthlyBill.id).where(
                MonthlyBill.room_id == room.id, MonthlyBill.period == period, MonthlyBill.cancelled_at.is_(None))):
            raise ValueError("Cần hủy phiếu chưa thu trước khi sửa ảnh công tơ; phiếu đã thu cần root xử lý.")
        existing = db.session.scalar(db.select(Photo).where(Photo.room_id == room.id, Photo.period == period))
    if existing and existing.status == "pending":
        raise ValueError("Ảnh công tơ đang xử lý. Hãy chờ hoàn tất trước khi thay ảnh.")
    photo = Photo(token=token or uuid.uuid4().hex, created_by=user_id)
    staged.append(photo)
    path = photo_path(photo, temporary=True)
    # Ignore the client filename and MIME; limit bytes before parsing image data.
    with path.open("xb") as destination:
        if os.name != "nt":
            os.chmod(path, 0o600)
        remaining = current_app.config["PHOTO_MAX_BYTES"]
        while chunk := upload.stream.read(min(65536, remaining + 1)):
            remaining -= len(chunk)
            if remaining < 0:
                raise ValueError("Mỗi ảnh tối đa 10 MB.")
            destination.write(chunk)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(path, formats=FORMATS) as image:
                if image.width * image.height > MAX_PIXELS or getattr(image, "n_frames", 1) != 1:
                    raise ValueError("Ảnh tối đa 24 megapixel và không được là ảnh động.")
                image.verify()
    except (UnidentifiedImageError, OSError, SyntaxError, Image.DecompressionBombError, Image.DecompressionBombWarning) as error:
        raise ValueError("Ảnh không hợp lệ. Chỉ nhận JPEG, PNG hoặc WebP.") from error
    if existing:
        existing.previous_token = existing.display_token
        existing.token = photo.token
        existing.status = "pending"
        existing.created_by, existing.created_at = user_id, utcnow()
        return existing
    photo.tenancy, photo.reading = tenancy, reading
    if room:
        photo.room_id, photo.period = room.id, period
    db.session.add(photo)
    return photo


def process_pending():
    """One worker only: jobs remain pending across termination/restart."""
    ids = db.session.scalars(db.select(Photo.id).where(Photo.status == "pending").order_by(Photo.id)).all()
    db.session.remove()
    for photo_id in ids:
        photo = db.session.get(Photo, photo_id)
        source, target = photo_path(photo, True), photo_path(photo)
        part = target.with_suffix(".part")
        try:
            # Atomic rename can have completed just before a previous worker exited.
            if not target.exists():
                with Image.open(source, formats=FORMATS) as image:
                    image = ImageOps.exif_transpose(image)
                    image.thumbnail((2200, 2200), Image.Resampling.LANCZOS)
                    image = image.convert("RGB")
                    image.info.clear()
                    image.save(part, "WEBP", quality=82, method=4, exif=b"", icc_profile=None)
                if os.name != "nt":
                    os.chmod(part, 0o600)
                os.replace(part, target)
            photo.status = "ready"
        except (OSError, ValueError, SyntaxError, Image.DecompressionBombError):
            photo.status = "failed"
            current_app.logger.error("Photo processing failed for job %s", photo_id)
        previous = photo.previous_token if photo.status == "ready" else None
        if previous:
            photo.previous_token = None
        db.session.commit()
        # Delete original only after persisting the final state; failed jobs need reupload.
        source.unlink(missing_ok=True)
        part.unlink(missing_ok=True)
        if previous:
            target.with_name(f"{previous}.webp").unlink(missing_ok=True)
        db.session.remove()
    cleanup_temporary()
    return len(ids)


def cleanup_temporary():
    """Recover crash leftovers, retaining pending jobs and recent staged uploads."""
    pending = set(db.session.scalars(db.select(Photo.token).where(Photo.status == "pending")))
    cutoff = time.time() - 3600
    for path in (photo_root() / "tmp").glob("*.upload"):
        if path.stem not in pending and path.stat().st_mtime < cutoff:
            path.unlink(missing_ok=True)
    referenced = set()
    for token, previous in db.session.execute(db.select(Photo.token, Photo.previous_token)):
        referenced.add(token)
        if previous:
            referenced.add(previous)
    # Recover obsolete outputs after a crash between DB commit and file deletion.
    for folder in ("contracts", "electricity"):
        for path in (photo_root() / folder).glob("*.webp"):
            if path.stem not in referenced and path.stat().st_mtime < cutoff:
                path.unlink(missing_ok=True)
    db.session.remove()


def register_commands(app):
    @app.cli.command("process-photos")
    @click.option("--once", is_flag=True, help="Process current queue then exit.")
    def process_photos(once):
        """Run exactly one durable photo compression worker per application."""
        # OS lock is released on crash; prevent simultaneous workers on Windows/Linux.
        with (photo_root() / "worker.lock").open("a+b") as lock:
            if lock.tell() == 0:
                lock.write(b"0")
                lock.flush()
            lock.seek(0)
            try:
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as error:
                raise click.ClickException("A photo worker is already running.") from error
            while True:
                count = process_pending()
                if once:
                    click.echo(f"Processed {count} photo jobs.")
                    return
                time.sleep(2)
