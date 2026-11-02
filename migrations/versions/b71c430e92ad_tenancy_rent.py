"""Add monthly rent to tenancy, retaining unknown legacy values.

Revision ID: b71c430e92ad
Revises: a65b2f9c018e
"""
from alembic import op
import sqlalchemy as sa

revision = 'b71c430e92ad'
down_revision = 'a65b2f9c018e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tenancy', sa.Column('rent_price', sa.Integer(), sa.CheckConstraint('rent_price IS NULL OR rent_price BETWEEN 0 AND 2147483647', name='ck_rent_price'), nullable=True))


def downgrade():
    op.drop_column('tenancy', 'rent_price')
