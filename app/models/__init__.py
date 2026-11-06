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
    meter_photos = db.relationship("Photo", foreign_keys="Photo.room_id", passive_deletes="all")

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
    move_in_date = db.Column(db.Date)
    move_out_date = db.Column(db.Date)
    contract_start = db.Column(db.Date)
    contract_end = db.Column(db.Date)
    contract_anchor_day = db.Column(db.Integer)
    water_price = db.Column(db.Integer)
    electricity_price = db.Column(db.Integer)
    service_price = db.Column(db.Integer)
    deposit_amount = db.Column(db.Integer)
    rent_price = db.Column(db.Integer)
    payment_day = db.Column(db.Integer)
    version = db.Column(db.Integer, nullable=False, default=1, server_default="1")
    room = db.relationship("Room", back_populates="tenancies")
    occupants = db.relationship("Occupant", cascade="all, delete-orphan", order_by="Occupant.id")
    vehicles = db.relationship("Vehicle", cascade="all, delete-orphan", order_by="Vehicle.id")
    renewals = db.relationship("ContractRenewal", order_by="ContractRenewal.id", back_populates="tenancy")
    photos = db.relationship("Photo", back_populates="tenancy", order_by="Photo.id")
    __mapper_args__ = {"version_id_col": version}
    __table_args__ = (
        db.CheckConstraint("water_price IS NULL OR water_price BETWEEN 0 AND 2147483647", name="ck_water_price"),
        db.CheckConstraint("electricity_price IS NULL OR electricity_price BETWEEN 0 AND 2147483647", name="ck_electricity_price"),
        db.CheckConstraint("service_price IS NULL OR service_price BETWEEN 0 AND 2147483647", name="ck_service_price"),
        db.CheckConstraint("deposit_amount IS NULL OR deposit_amount BETWEEN 0 AND 2147483647", name="ck_deposit_amount"),
        db.CheckConstraint("rent_price IS NULL OR rent_price BETWEEN 0 AND 2147483647", name="ck_rent_price"),
        db.CheckConstraint("payment_day IS NULL OR payment_day BETWEEN 1 AND 31", name="ck_payment_day"),
        db.CheckConstraint("contract_anchor_day IS NULL OR contract_anchor_day BETWEEN 1 AND 31", name="ck_contract_anchor"),
        db.CheckConstraint("contract_end IS NULL OR contract_start IS NULL OR contract_end >= contract_start", name="ck_contract_dates"),
        db.CheckConstraint("move_out_date IS NULL OR move_in_date IS NULL OR move_out_date >= move_in_date", name="ck_move_dates"),
    )

    @property
    def monthly_fees(self):
        if self.water_price is None or self.service_price is None:
            return None
        return self.water_price * self.people_count + self.service_price

    @property
    def monthly_total(self):
        fees = self.monthly_fees
        return self.rent_price + fees if self.rent_price is not None and fees is not None else None

    @property
    def people_count(self):
        return 1 + len(self.occupants)


db.Index("uq_room_open_tenancy", Tenancy.room_id, unique=True, sqlite_where=Tenancy.ended_at.is_(None), postgresql_where=Tenancy.ended_at.is_(None))


class ContractRenewal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenancy_id = db.Column(db.Integer, db.ForeignKey("tenancy.id", ondelete="RESTRICT"), nullable=False)
    old_end = db.Column(db.Date, nullable=False)
    new_end = db.Column(db.Date, nullable=False)
    months = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(1000), nullable=False, default="")
    created_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    tenancy = db.relationship("Tenancy", back_populates="renewals")
    author = db.relationship("User")
    __table_args__ = (
        db.UniqueConstraint("tenancy_id", "old_end", name="uq_renewal_old_end"),
        db.CheckConstraint("months BETWEEN 1 AND 120 AND new_end > old_end", name="ck_renewal"),
    )


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
    electricity_price = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    room = db.relationship("Room", back_populates="readings")
    photos = db.relationship("Photo", back_populates="reading", order_by="Photo.id")
    __table_args__ = (
        db.UniqueConstraint("room_id", "period", name="uq_room_period"),
        db.CheckConstraint("start_value >= 0 AND end_value >= start_value", name="ck_valid_reading"),
        db.CheckConstraint("electricity_price IS NULL OR electricity_price BETWEEN 0 AND 2147483647", name="ck_reading_price"),
    )

    @property
    def consumption(self):
        return self.end_value - self.start_value


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), unique=True, nullable=False)
    previous_token = db.Column(db.String(32))
    tenancy_id = db.Column(db.Integer, db.ForeignKey("tenancy.id", ondelete="RESTRICT"))
    reading_id = db.Column(db.Integer, db.ForeignKey("electricity_reading.id", ondelete="RESTRICT"))
    room_id = db.Column(db.Integer, db.ForeignKey("room.id", ondelete="RESTRICT"))
    period = db.Column(db.String(7))
    status = db.Column(db.String(16), nullable=False, default="pending")
    created_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    tenancy = db.relationship("Tenancy", back_populates="photos")
    reading = db.relationship("ElectricityReading", back_populates="photos")
    __table_args__ = (
        db.Index("uq_photo_reading", "reading_id", unique=True),
        db.Index("uq_photo_room_period", "room_id", "period", unique=True),
        db.CheckConstraint("(tenancy_id IS NOT NULL AND reading_id IS NULL AND room_id IS NULL AND period IS NULL) OR (tenancy_id IS NULL AND reading_id IS NOT NULL AND room_id IS NULL AND period IS NULL) OR (tenancy_id IS NULL AND reading_id IS NULL AND room_id IS NOT NULL AND period IS NOT NULL)", name="ck_photo_owner"),
        db.CheckConstraint("status IN ('pending', 'ready', 'failed')", name="ck_photo_status"),
    )

    @property
    def display_token(self):
        return self.token if self.status == "ready" else self.previous_token


class ReadingRevision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reading_id = db.Column(db.Integer, db.ForeignKey("electricity_reading.id", ondelete="RESTRICT"), nullable=False)
    old_start = db.Column(db.Integer, nullable=False)
    old_end = db.Column(db.Integer, nullable=False)
    new_start = db.Column(db.Integer, nullable=False)
    new_end = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(500), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    author = db.relationship("User")


class MonthlyBill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id", ondelete="RESTRICT"), nullable=False)
    tenancy_id = db.Column(db.Integer, db.ForeignKey("tenancy.id", ondelete="RESTRICT"), nullable=False)
    period = db.Column(db.String(7), nullable=False)
    tenant_name = db.Column(db.String(120), nullable=False)
    room_code = db.Column(db.String(30), nullable=False)
    start_value = db.Column(db.Integer, nullable=False)
    end_value = db.Column(db.Integer, nullable=False)
    rent_price = db.Column(db.Integer, nullable=False)
    water_price = db.Column(db.Integer, nullable=False)
    service_price = db.Column(db.Integer, nullable=False)
    electricity_price = db.Column(db.Integer, nullable=False)
    people_count = db.Column(db.Integer, nullable=False)
    final_amount = db.Column(db.BigInteger)
    adjustment_reason = db.Column(db.String(500), nullable=False, default="", server_default="")
    due_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    cancelled_at = db.Column(db.DateTime)
    cancelled_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="RESTRICT"))
    cancel_reason = db.Column(db.String(500))
    receipts = db.relationship("Receipt", back_populates="bill", order_by="Receipt.id")
    __table_args__ = (
        db.CheckConstraint("final_amount IS NULL OR final_amount >= 0", name="ck_bill_final_amount"),
        db.CheckConstraint("start_value >= 0 AND end_value >= start_value AND rent_price >= 0 AND water_price >= 0 AND service_price >= 0 AND electricity_price >= 0 AND people_count BETWEEN 1 AND 31", name="ck_bill_values"),
    )

    @property
    def computed_total(self):
        return self.rent_price + self.water_total + self.service_price + self.electricity_total

    @property
    def consumption(self):
        return self.end_value - self.start_value

    @property
    def water_total(self):
        return self.water_price * self.people_count

    @property
    def electricity_total(self):
        return self.consumption * self.electricity_price

    @property
    def total(self):
        return self.final_amount if self.final_amount is not None else self.computed_total

    @property
    def adjustment_amount(self):
        return self.total - self.computed_total

    @property
    def paid_receipt(self):
        return next((r for r in self.receipts if r.reversed_at is None), None)


class BillChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    old_bill_id = db.Column(db.Integer, db.ForeignKey('monthly_bill.id', ondelete='RESTRICT'), nullable=False, unique=True)
    new_bill_id = db.Column(db.Integer, db.ForeignKey('monthly_bill.id', ondelete='RESTRICT'), nullable=False, unique=True)
    reason = db.Column(db.String(500), nullable=False, default='')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='RESTRICT'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    old_bill = db.relationship('MonthlyBill', foreign_keys=[old_bill_id])
    new_bill = db.relationship('MonthlyBill', foreign_keys=[new_bill_id])
    author = db.relationship('User')


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey("monthly_bill.id", ondelete="RESTRICT"), nullable=False)
    amount = db.Column(db.BigInteger, nullable=False)
    paid_date = db.Column(db.Date, nullable=False)
    note = db.Column(db.String(500), nullable=False, default="")
    created_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="RESTRICT"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    reversed_at = db.Column(db.DateTime)
    reversed_by = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="RESTRICT"))
    reverse_reason = db.Column(db.String(500))
    bill = db.relationship("MonthlyBill", back_populates="receipts")
    author = db.relationship("User", foreign_keys=[created_by])
    reverser = db.relationship("User", foreign_keys=[reversed_by])
    __table_args__ = (db.CheckConstraint("amount >= 0", name="ck_receipt_amount"),)


db.Index("uq_active_receipt", Receipt.bill_id, unique=True,
         sqlite_where=Receipt.reversed_at.is_(None), postgresql_where=Receipt.reversed_at.is_(None))


class PaymentSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auto_transfer_content = db.Column(db.Boolean, nullable=False, default=True, server_default=db.true())
    bank_bin = db.Column(db.String(6))
    bank_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)
    account_name = db.Column(db.String(150), nullable=False)
    note = db.Column(db.String(300), nullable=False)
    qr_token = db.Column(db.String(32))


db.Index("uq_active_bill", MonthlyBill.room_id, MonthlyBill.period, unique=True,
         sqlite_where=MonthlyBill.cancelled_at.is_(None), postgresql_where=MonthlyBill.cancelled_at.is_(None))
