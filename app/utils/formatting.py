import re
from datetime import date, datetime, timedelta, timezone

VIETNAM_TZ = timezone(timedelta(hours=7))


def local_today():
    return datetime.now(VIETNAM_TZ).date()


def money_digits(value):
    value = str(value).strip()
    if value.endswith('đ'):
        value = value[:-1].strip()
    if not re.fullmatch(r'(?:[0-9]+|[0-9]{1,3}(?:\.[0-9]{3})+)', value):
        raise ValueError('Số tiền cần là số nguyên, ví dụ 1.000.000 đ.')
    return value.replace('.', '')


def parse_money(value, label, maximum=2147483647, required=False):
    if value == '':
        if required:
            raise ValueError(f'{label} là bắt buộc; nhập 0 nếu miễn phí.')
        return None
    raw = money_digits(value)
    if len(raw) > 19 or int(raw) > maximum:
        raise ValueError(f'{label} vượt giới hạn {vnd(maximum)}.')
    return int(raw)


def vnd(value):
    return f'{value:,}'.replace(',', '.') + ' đ' if value is not None else 'Chưa cập nhật'


def money_input(value):
    if value is None or value == '':
        return ''
    try:
        return vnd(int(money_digits(value)))
    except ValueError:
        return value


def read_date(value):
    if isinstance(value, date):
        return value
    if re.fullmatch(r'[0-9]{2}/[0-9]{2}/[0-9]{4}', value or ''):
        day, month, year = map(int, value.split('/'))
        return date(year, month, day)
    if re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', value or ''):
        return date.fromisoformat(value)
    raise ValueError('Ngày cần có dạng dd/mm/yyyy.')


def business_date(value):
    return read_date(value).strftime('%d/%m/%Y') if value else 'Chưa cập nhật'


def date_input(value):
    if not value:
        return ''
    try:
        return business_date(value)
    except ValueError:
        return value


def local_datetime(value):
    if not value:
        return '—'
    return (value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value).astimezone(VIETNAM_TZ)


def period_label(value):
    return f'{value[5:]}/{value[:4]}' if re.fullmatch(r'[12][0-9]{3}-(0[1-9]|1[0-2])', value or '') else value


def register_filters(app):
    app.jinja_env.filters.update(vnd=vnd, money_input=money_input, business_date=business_date,
        date_input=date_input, period_label=period_label,
        local_date=lambda value: local_datetime(value).strftime('%d/%m/%Y') if value else '—',
        local_datetime=lambda value: local_datetime(value).strftime('%d/%m/%Y %H:%M:%S') if value else '—')
