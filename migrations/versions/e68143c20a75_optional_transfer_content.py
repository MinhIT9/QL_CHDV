"""Allow administrators to omit prefilled QR transfer content."""
from alembic import op
import sqlalchemy as sa

revision = 'e68143c20a75'
down_revision = 'd57032b19f64'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('payment_settings', sa.Column('auto_transfer_content', sa.Boolean(), nullable=False, server_default=sa.true()))


def downgrade():
    op.drop_column('payment_settings', 'auto_transfer_content')
