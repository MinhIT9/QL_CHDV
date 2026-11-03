"""Keep the electricity estimate rate with each saved reading."""
from alembic import op
import sqlalchemy as sa

revision = 'd94f512a37b1'
down_revision = 'c83e4d16b2a0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('electricity_reading', sa.Column('electricity_price', sa.Integer(), sa.CheckConstraint('electricity_price IS NULL OR electricity_price BETWEEN 0 AND 2147483647', name='ck_reading_price'), nullable=True))
    op.execute("""UPDATE electricity_reading SET electricity_price = (
        SELECT electricity_price FROM monthly_bill
        WHERE monthly_bill.room_id = electricity_reading.room_id
          AND monthly_bill.period = electricity_reading.period
          AND monthly_bill.cancelled_at IS NULL)
        WHERE EXISTS (SELECT 1 FROM monthly_bill
          WHERE monthly_bill.room_id = electricity_reading.room_id
            AND monthly_bill.period = electricity_reading.period
            AND monthly_bill.cancelled_at IS NULL)""")


def downgrade():
    op.drop_column('electricity_reading', 'electricity_price')
