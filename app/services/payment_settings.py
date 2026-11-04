import secrets
import warnings
from io import BytesIO
from pathlib import Path

from flask import current_app
from PIL import Image, ImageOps, UnidentifiedImageError

from app.extensions import db
from app.models import PaymentSettings


def payment_settings():
    return db.session.get(PaymentSettings, 1)


def qr_path(token):
    return Path(current_app.config['PHOTO_ROOT']) / 'payment' / f'{token}.png'


def save_payment_settings(form, upload):
    values = {}
    for key, limit in [('bank_name', 100), ('account_number', 50), ('account_name', 150), ('note', 300)]:
        value = form.get(key, '').strip()
        if len(value) > limit:
            raise ValueError('Thông tin nhận tiền quá dài.')
        values[key] = value
    if not all(values[key] for key in ('bank_name', 'account_number', 'account_name')):
        raise ValueError('Điền ngân hàng, số tài khoản và tên chủ tài khoản.')
    settings = payment_settings() or PaymentSettings(id=1)
    old_token = settings.qr_token
    token = None
    if upload and upload.filename:
        raw = upload.stream.read(5 * 1024 * 1024 + 1)
        if len(raw) > 5 * 1024 * 1024:
            raise ValueError('Ảnh QR tối đa 5 MB.')
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('error', Image.DecompressionBombWarning)
                with Image.open(BytesIO(raw)) as image:
                    if image.format not in {'PNG', 'JPEG', 'WEBP'} or max(image.size) > 4096:
                        raise ValueError('Dùng ảnh PNG/JPG/WebP tối đa 4096 px.')
                    image.load()
                    # Lossless PNG preserves QR edges; discard metadata and original bytes.
                    image = ImageOps.exif_transpose(image).convert('RGB')
                    token = secrets.token_hex(16)
                    path = qr_path(token)
                    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                    image.save(path, format='PNG', optimize=True)
                    path.chmod(0o600)
        except (UnidentifiedImageError, Image.DecompressionBombError, Image.DecompressionBombWarning, OSError) as error:
            if token:
                qr_path(token).unlink(missing_ok=True)
            raise ValueError('Không đọc được ảnh QR hợp lệ.') from error
    try:
        for key, value in values.items():
            setattr(settings, key, value)
        settings.qr_token = token or (None if form.get('remove_qr') == '1' else old_token)
        db.session.add(settings)
        db.session.commit()
    except Exception:
        db.session.rollback()
        if token:
            qr_path(token).unlink(missing_ok=True)
        raise
    if old_token and old_token != settings.qr_token:
        qr_path(old_token).unlink(missing_ok=True)
    return settings
