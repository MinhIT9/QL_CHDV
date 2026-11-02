"""Add tenancy deposit and use contract_start as the sole business start date.

Revision ID: a65b2f9c018e
Revises: dd7493777e83
"""
from alembic import op
import sqlalchemy as sa

revision = 'a65b2f9c018e'
down_revision = 'dd7493777e83'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tenancy', sa.Column('deposit_amount', sa.Integer(), sa.CheckConstraint('deposit_amount IS NULL OR deposit_amount BETWEEN 0 AND 2147483647', name='ck_deposit_amount'), nullable=True))
    # Prefer an explicit contract start. Use the former move-in only when no
    # start is recorded and it does not conflict with recorded end/checkout.
    # Keep the old column as legacy data, avoiding destructive table rebuilds.
    op.execute("""UPDATE tenancy SET contract_start = move_in_date, version = version + 1
                  WHERE contract_start IS NULL AND move_in_date IS NOT NULL
                    AND (contract_end IS NULL OR move_in_date <= contract_end)
                    AND (move_out_date IS NULL OR move_in_date <= move_out_date)""")


def downgrade():
    op.drop_column('tenancy', 'deposit_amount')
    # Backfilled start dates remain: we cannot distinguish later manual edits.
