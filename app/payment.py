from flask import Blueprint, abort, flash, redirect, render_template, request, send_file, url_for
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db

from app.services.payment_settings import payment_settings, qr_path, save_payment_settings
from app.services.vietqr import BANKS, BANK_BY_BIN, payload, qr_png

bp = Blueprint('payment', __name__, url_prefix='/settings/payment')


@bp.route('', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        try:
            save_payment_settings(request.form)
        except ValueError as error:
            flash(str(error), 'danger')
            return render_template('payment/settings.html', values=request.form, settings=payment_settings(), banks=BANKS), 400
        except (OSError, SQLAlchemyError):
            db.session.rollback()
            flash('Không thể lưu thông tin nhận tiền. Vui lòng thử lại.', 'danger')
            return render_template('payment/settings.html', values=request.form, settings=payment_settings(), banks=BANKS), 503
        flash('Đã lưu thông tin nhận tiền. Vui lòng quét thử QR để kiểm tra đúng tài khoản.', 'success')
        return redirect(url_for('payment.settings'))
    settings = payment_settings()
    return render_template('payment/settings.html', values=settings, settings=settings, banks=BANKS)


@bp.get('/qr')
@login_required
def generated_qr():
    settings = payment_settings()
    if not settings or settings.bank_bin not in BANK_BY_BIN:
        abort(404)
    return send_file(qr_png(payload(settings.bank_bin, settings.account_number)), mimetype='image/png', max_age=0)


@bp.get('/qr/<token>')
@login_required
def qr(token):
    settings = payment_settings()
    if not settings or token != settings.qr_token:
        abort(404)
    path = qr_path(token)
    if not path.is_file():
        abort(404)
    return send_file(path, mimetype='image/png', max_age=0)
