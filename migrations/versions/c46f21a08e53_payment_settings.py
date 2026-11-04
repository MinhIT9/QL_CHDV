"""Shared receiving account and private QR image reference."""
from alembic import op
import sqlalchemy as sa

revision = 'c46f21a08e53'
down_revision = 'b35e10f97d42'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('payment_settings',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('bank_name', sa.String(100), nullable=False),
                    sa.Column('account_number', sa.String(50), nullable=False),
                    sa.Column('account_name', sa.String(150), nullable=False),
                    sa.Column('note', sa.String(300), nullable=False),
                    sa.Column('qr_token', sa.String(32)))


def downgrade():
    op.drop_table('payment_settings')
