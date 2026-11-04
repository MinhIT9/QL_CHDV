import re
from pathlib import Path

from flask import current_app

from app.extensions import db
from app.models import PaymentSettings
from app.services.vietqr import BANK_BY_BIN


def payment_settings():
    return db.session.get(PaymentSettings, 1)


def qr_path(token):
    return Path(current_app.config['PHOTO_ROOT']) / 'payment' / f'{token}.png'


def save_payment_settings(form):
    bank = BANK_BY_BIN.get(form.get('bank_bin', ''))
    if not bank:
        raise ValueError('Chọn ngân hàng trong danh sách.')
    values = {'bank_bin': bank['bin'], 'bank_name': bank['short_name']}
    for key, limit in [('account_number', 19), ('account_name', 150), ('note', 300)]:
        value = form.get(key, '').strip()
        if len(value) > limit:
            raise ValueError('Thông tin nhận tiền quá dài.')
        values[key] = value
    if not re.fullmatch(r'[A-Za-z0-9]{1,19}', values['account_number']):
        raise ValueError('Số tài khoản cần 1–19 chữ số hoặc chữ cái, không có khoảng trắng.')
    if not values['account_name']:
        raise ValueError('Điền tên chủ tài khoản.')
    settings = payment_settings() or PaymentSettings(id=1)
    for key, value in values.items():
        setattr(settings, key, value)
    db.session.add(settings)
    db.session.commit()
    return settings
