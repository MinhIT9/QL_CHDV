import re
from datetime import datetime, timedelta
from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models import User

bp = Blueprint("auth", __name__)
DUMMY_HASH = generate_password_hash("not-an-account-password", method="scrypt")


def root_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_root:
            abort(403)
        return view(*args, **kwargs)
    return wrapped


def password_error(password):
    if len(password) < 8 or len(password) > 128:
        return "Mật khẩu phải từ 8 đến 128 ký tự."
    if password != password.strip() or not password.strip():
        return "Mật khẩu không được có khoảng trắng ở đầu hoặc cuối."
    return None


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("rooms.index"))
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        user = db.session.scalar(db.select(User).where(User.username == username))
        now = datetime.utcnow()
        valid = user.check_password(password) if user and len(password) <= 128 else check_password_hash(DUMMY_HASH, password[:128])
        locked = user and user.locked_until and user.locked_until > now
        if not user or not valid or not user.enabled or locked:
            if user and not locked:
                user.failed_logins += 1
                if user.failed_logins >= 5:
                    user.locked_until = now + timedelta(minutes=5)
                    user.failed_logins = 0
                db.session.commit()
            flash("Đăng nhập không thành công. Kiểm tra thông tin hoặc thử lại sau nếu tài khoản bị khóa.", "danger")
            return render_template("auth/login.html"), 401
        user.failed_logins = 0
        user.locked_until = None
        db.session.commit()
        session.clear()
        login_user(user)
        session.permanent = True
        return redirect(url_for("auth.change_password" if user.must_change_password else "rooms.index"))
    return render_template("auth/login.html")


@bp.post("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old = request.form.get("current_password", "")
        new = request.form.get("new_password", "")
        error = password_error(new)
        if not current_user.check_password(old[:128]) or len(old) > 128:
            error = "Mật khẩu hiện tại chưa đúng."
        elif new != request.form.get("confirm_password", ""):
            error = "Xác nhận mật khẩu không khớp."
        elif current_user.check_password(new):
            error = "Mật khẩu mới phải khác mật khẩu hiện tại."
        if error:
            flash(error, "danger")
            return render_template("auth/change_password.html"), 400
        user = current_user._get_current_object()
        user.set_password(new)
        user.must_change_password = False
        db.session.commit()
        # Rotate the identity token to invalidate all older sessions, then sign in this one.
        session.clear()
        login_user(user)
        session.permanent = True
        flash("Đã đổi mật khẩu.", "success")
        return redirect(url_for("rooms.index"))
    return render_template("auth/change_password.html")


@bp.route("/accounts", methods=["GET", "POST"])
@root_required
def accounts():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        error = password_error(password)
        if not re.fullmatch(r"[a-z0-9][a-z0-9_.-]{2,63}", username):
            error = "Tài khoản gồm 3–64 ký tự: chữ thường, số, dấu chấm, gạch ngang hoặc gạch dưới."
        if error:
            flash(error, "danger")
        else:
            user = User(username=username, must_change_password=True, is_root=False)
            user.set_password(password)
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash("Tên tài khoản đã tồn tại.", "danger")
            else:
                flash("Đã tạo Admin. Người dùng phải đổi mật khẩu trong lần đăng nhập đầu.", "success")
                return redirect(url_for("auth.accounts"))
        return render_template("auth/accounts.html", users=db.session.scalars(db.select(User).order_by(User.id)).all()), 400
    return render_template("auth/accounts.html", users=db.session.scalars(db.select(User).order_by(User.id)).all())


@bp.post("/accounts/<int:user_id>/toggle")
@root_required
def toggle_account(user_id):
    user = db.get_or_404(User, user_id)
    if user.is_root:
        abort(403)
    user.enabled = not user.enabled
    # Invalidate pre-existing sessions on both disable and enable.
    import secrets
    user.session_token = secrets.token_hex(32)
    db.session.commit()
    flash("Đã cập nhật trạng thái tài khoản.", "success")
    return redirect(url_for("auth.accounts"))


@bp.post("/accounts/<int:user_id>/reset-password")
@root_required
def reset_password(user_id):
    user = db.get_or_404(User, user_id)
    if user.is_root:
        abort(403)
    password = request.form.get("password", "")
    error = password_error(password)
    if error:
        flash(error, "danger")
    else:
        user.set_password(password)
        user.must_change_password = True
        user.failed_logins = 0
        user.locked_until = None
        db.session.commit()
        flash("Đã đặt lại mật khẩu. Người dùng phải đổi mật khẩu khi đăng nhập lại.", "success")
    return redirect(url_for("auth.accounts"))
