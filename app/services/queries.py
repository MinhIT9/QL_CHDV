"""Shared read queries; callers retain their own filtering and permissions."""

from sqlalchemy.orm import selectinload

from app.extensions import db
from app.models import BillChange, MonthlyBill, Room, Tenancy


def room_query():
    return db.select(Room).options(
        selectinload(Room.tenancies).selectinload(Tenancy.occupants),
        selectinload(Room.tenancies).selectinload(Tenancy.vehicles),
        selectinload(Room.readings),
    ).order_by(Room.code)


def active_bill_query():
    return db.select(MonthlyBill).where(MonthlyBill.cancelled_at.is_(None))


def bill_history_query(room_id):
    return db.select(MonthlyBill).options(selectinload(MonthlyBill.receipts)).where(
        MonthlyBill.room_id == room_id
    ).order_by(MonthlyBill.period.desc(), MonthlyBill.id.desc())


def bill_change_query(room_id, period=None):
    query = db.select(BillChange).join(BillChange.new_bill).options(
        selectinload(BillChange.old_bill), selectinload(BillChange.new_bill), selectinload(BillChange.author)
    ).where(MonthlyBill.room_id == room_id)
    if period:
        query = query.where(MonthlyBill.period == period)
    return query.order_by(BillChange.id.desc())
