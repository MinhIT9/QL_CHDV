"""Explicit bank BIN for local VietQR; preserve legacy uploaded QR."""
from alembic import op
import sqlalchemy as sa

revision = 'd57032b19f64'
down_revision = 'c46f21a08e53'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('payment_settings', sa.Column('bank_bin', sa.String(6)))


def downgrade():
    op.drop_column('payment_settings', 'bank_bin')
