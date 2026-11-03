"""Shared read queries; callers retain their own filtering and permissions."""

from sqlalchemy.orm import selectinload

from app.extensions import db
from app.models import MonthlyBill, Room, Tenancy


def room_query():
    return db.select(Room).options(
        selectinload(Room.tenancies).selectinload(Tenancy.occupants),
        selectinload(Room.tenancies).selectinload(Tenancy.vehicles),
        selectinload(Room.readings),
    ).order_by(Room.code)


def active_bill_query():
    return db.select(MonthlyBill).where(MonthlyBill.cancelled_at.is_(None))
