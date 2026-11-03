import os
from datetime import timedelta, timezone
from pathlib import Path

import click
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, logout_user
from sqlalchemy import event
from werkzeug.exceptions import HTTPException

from app.extensions import csrf, db, login_manager, migrate


def create_app(test_config=None):
    root = Path(__file__).resolve().parents[1]
    if test_config is None:
        load_dotenv(root / ".env")
    app = Flask(__name__, instance_path=str(root / "instance"))
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///chdv.sqlite3"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "false").lower() == "true",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
        MAX_CONTENT_LENGTH=256 * 1024,
        WTF_CSRF_TIME_LIMIT=8 * 60 * 60,
    )
    if test_config:
        app.config.update(test_config)
    if not app.config["SECRET_KEY"]:
        raise RuntimeError("SECRET_KEY is required. Create .env using .env.example.")
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Vui lòng đăng nhập để tiếp tục."
    migrate.init_app(app, db, render_as_batch=True)

    from app.models import User
    from app.auth.routes import bp as auth_bp
    from app.rooms.routes import bp as rooms_bp
    from app.electricity.routes import bp as electricity_bp
    from app.electricity.billing_routes import bp as billing_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(electricity_bp)
    app.register_blueprint(billing_bp)

    with app.app_context():
        if db.engine.dialect.name == "sqlite":
            @event.listens_for(db.engine, "connect")
            def sqlite_settings(connection, _record):
                cursor = connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA busy_timeout=5000")
                cursor.close()

    @login_manager.user_loader
    def load_user(token):
        return db.session.scalar(db.select(User).where(User.session_token == token, User.enabled.is_(True)))

    @app.before_request
    def enforce_password_change():
        if current_user.is_authenticated:
            if not current_user.enabled:
                logout_user()
                session.clear()
                return redirect(url_for("auth.login"))
            if current_user.must_change_password and request.endpoint not in {
                "auth.change_password", "auth.logout", "static",
            }:
                flash("Bạn cần đổi mật khẩu trước khi sử dụng ứng dụng.", "warning")
                return redirect(url_for("auth.change_password"))

    @app.after_request
    def security_headers(response):
        if request.headers.get("HX-Request") and response.status_code in {301, 302, 303, 307, 308}:
            response.headers["HX-Redirect"] = response.headers.pop("Location")
            response.status_code = 200
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' https://cdn.jsdelivr.net; script-src 'self' https://cdn.jsdelivr.net; img-src 'self' data:; base-uri 'self'; form-action 'self'; frame-ancestors 'none'"
        if request.endpoint != "static":
            response.headers["Cache-Control"] = "no-store"
        return response

    @app.template_filter("local_date")
    def local_date(value):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone(timedelta(hours=7))).strftime("%d/%m/%Y")

    @app.template_filter("business_date")
    def business_date(value):
        return value.strftime("%d/%m/%Y") if value else "Chưa cập nhật"

    @app.template_filter("local_datetime")
    def local_datetime(value):
        if value is None:
            return "—"
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone(timedelta(hours=7))).strftime("%d/%m/%Y %H:%M:%S")

    @app.template_filter("vnd")
    def vnd(value):
        return f"{value:,}".replace(",", ".") + " đ" if value is not None else "Chưa cập nhật"

    @app.errorhandler(HTTPException)
    def http_error(error):
        return render_template("error.html", code=error.code, message={
            400: "Yêu cầu không hợp lệ hoặc phiên nhập liệu đã hết hạn. Vui lòng tải lại trang.",
            403: "Bạn không có quyền thực hiện thao tác này.",
            404: "Không tìm thấy thông tin yêu cầu.",
            413: "Dữ liệu gửi lên quá lớn.",
        }.get(error.code, error.description)), error.code

    @app.cli.command("init-admin")
    def init_admin():
        """Create initial root once; never overwrite an existing password."""
        username = os.environ.get("INITIAL_ADMIN_USERNAME", "root").strip().lower()
        password = os.environ.get("INITIAL_ADMIN_PASSWORD", "")
        if db.session.scalar(db.select(User).where(User.username == username)):
            click.echo("Initial administrator already exists; no changes made.")
            return
        if username != "root" or len(password) < 8:
            raise click.ClickException("Set INITIAL_ADMIN_USERNAME=root and an initial password of at least 8 characters in .env.")
        user = User(username=username, is_root=True, must_change_password=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo("Initial root created. Password change required on first login.")

    @app.cli.command("backup-db")
    @click.argument("destination", type=click.Path(path_type=Path))
    def backup_db(destination):
        """Create a consistent SQLite backup to a NEW destination file."""
        import sqlite3
        from contextlib import closing
        if db.engine.dialect.name != "sqlite":
            raise click.ClickException("This command supports SQLite only.")
        source = Path(db.engine.url.database).resolve()
        destination = destination.resolve()
        if not source.is_file() or destination.exists() or source == destination:
            raise click.ClickException("Source must exist and destination must be a new file.")
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation prevents silently overwriting another backup.
        destination.touch(exist_ok=False)
        with closing(sqlite3.connect(str(source))) as source_db, closing(sqlite3.connect(str(destination))) as target_db:
            source_db.backup(target_db)
        click.echo("SQLite backup completed.")

    return app
