import secrets
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


def utcnow():
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_root = db.Column(db.Boolean, nullable=False, default=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    must_change_password = db.Column(db.Boolean, nullable=False, default=True)
    session_token = db.Column(db.String(64), unique=True, nullable=False, default=lambda: secrets.token_hex(32))
    failed_logins = db.Column(db.Integer, nullable=False, default=0)
    locked_until = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)

    @property
    def is_active(self):
        return self.enabled

    def get_id(self):
        return self.session_token

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="scrypt")
        self.session_token = secrets.token_hex(32)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    note = db.Column(db.Text, nullable=False, default="")
    tenancies = db.relationship("Tenancy", back_populates="room", order_by="Tenancy.id")
    readings = db.relationship("ElectricityReading", back_populates="room", order_by="ElectricityReading.period")

    @property
    def current_tenancy(self):
        return next((item for item in reversed(self.tenancies) if item.ended_at is None), None)

    @property
    def status(self):
        if not self.active:
            return "Ngừng sử dụng"
        return "Đang thuê" if self.current_tenancy else "Trống"


class Tenancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id", ondelete="RESTRICT"), nullable=False)
    tenant_name = db.Column(db.String(120), nullable=False)
    started_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    ended_at = db.Column(db.DateTime)
    room = db.relationship("Room", back_populates="tenancies")
    occupants = db.relationship("Occupant", cascade="all, delete-orphan", order_by="Occupant.id")
    vehicles = db.relationship("Vehicle", cascade="all, delete-orphan", order_by="Vehicle.id")

    @property
    def people_count(self):
        return 1 + len(self.occupants)


db.Index("uq_room_open_tenancy", Tenancy.room_id, unique=True, sqlite_where=Tenancy.ended_at.is_(None), postgresql_where=Tenancy.ended_at.is_(None))


class Occupant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenancy_id = db.Column(db.Integer, db.ForeignKey("tenancy.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(120), nullable=False)


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenancy_id = db.Column(db.Integer, db.ForeignKey("tenancy.id", ondelete="CASCADE"), nullable=False)
    plate = db.Column(db.String(30), nullable=False)


class ElectricityReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id", ondelete="RESTRICT"), nullable=False)
    period = db.Column(db.String(7), nullable=False)
    start_value = db.Column(db.Integer, nullable=False)
    end_value = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    room = db.relationship("Room", back_populates="readings")
    __table_args__ = (
        db.UniqueConstraint("room_id", "period", name="uq_room_period"),
        db.CheckConstraint("start_value >= 0 AND end_value >= start_value", name="ck_valid_reading"),
    )

    @property
    def consumption(self):
        return self.end_value - self.start_value
