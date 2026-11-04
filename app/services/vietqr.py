"""Local NAPAS account-transfer TLV payload and QR rendering; no network calls."""
import binascii
import json
import re
import unicodedata
from io import BytesIO
from pathlib import Path

import qrcode

BANKS = json.loads((Path(__file__).resolve().parents[1] / 'data' / 'banks.json').read_text(encoding='utf-8'))
BANK_BY_BIN = {bank['bin']: bank for bank in BANKS}
MAX_QR_AMOUNT = 9_999_999_999_999


def field(tag, value):
    length = len(value.encode('ascii'))
    if length > 99:
        raise ValueError('Dữ liệu QR quá dài.')
    return f'{tag}{length:02d}{value}'


def transfer_content(bill, enabled=True):
    if not enabled:
        return ''
    room = unicodedata.normalize('NFKD', bill.room_code.replace('đ', 'd').replace('Đ', 'D')).encode('ascii', 'ignore').decode()
    room = re.sub(r'[^A-Za-z0-9]', '', room).upper()[:12]
    return f'P{bill.id} {room} T{bill.period[5:]}{bill.period[:4]}'[:50]


def payload(bank_bin, account, amount=None, content=''):
    if bank_bin not in BANK_BY_BIN or not re.fullmatch(r'[A-Za-z0-9]{1,19}', account):
        raise ValueError('Ngân hàng hoặc số tài khoản không hợp lệ.')
    if amount is not None and (type(amount) is not int or not 0 < amount <= MAX_QR_AMOUNT):
        raise ValueError('Số tiền vượt giới hạn QR hoặc không cần thanh toán.')
    if not re.fullmatch(r'[A-Za-z0-9 .\-/]{0,50}', content):
        raise ValueError('Nội dung QR không hợp lệ.')
    recipient = field('00', bank_bin) + field('01', account)
    provider = field('00', 'A000000727') + field('01', recipient) + field('02', 'QRIBFTTA')
    value = field('00', '01') + field('01', '12' if amount is not None else '11') + field('38', provider) + field('53', '704')
    if amount is not None:
        value += field('54', str(amount))
    value += field('58', 'VN')
    if content:
        value += field('62', field('08', content))
    value += '6304'
    return value + f'{binascii.crc_hqx(value.encode("ascii"), 0xFFFF):04X}'


def qr_png(value):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=4)
    qr.add_data(value, optimize=0)
    qr.make(fit=True)
    output = BytesIO()
    qr.make_image(fill_color='black', back_color='white').save(output, format='PNG')
    output.seek(0)
    return output


def bill_qr_enabled(settings, bill):
    return bool(settings and settings.bank_bin in BANK_BY_BIN and not bill.cancelled_at
                and not bill.paid_receipt and 0 < bill.total <= MAX_QR_AMOUNT)
