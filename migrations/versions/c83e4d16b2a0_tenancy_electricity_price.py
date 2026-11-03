"""Store the default electricity unit price with tenancy terms."""
from alembic import op
import sqlalchemy as sa

revision = 'c83e4d16b2a0'
down_revision = '0fecdf9f864b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tenancy', sa.Column('electricity_price', sa.Integer(), sa.CheckConstraint('electricity_price IS NULL OR electricity_price BETWEEN 0 AND 2147483647', name='ck_electricity_price'), nullable=True))


def downgrade():
    op.drop_column('tenancy', 'electricity_price')
