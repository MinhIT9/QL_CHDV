"""Persist explicit bill replacement audit links and reasons."""
from alembic import op
import sqlalchemy as sa

revision = 'f79254d31b86'
down_revision = 'e68143c20a75'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('bill_change',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('old_bill_id', sa.Integer(), sa.ForeignKey('monthly_bill.id', ondelete='RESTRICT'), nullable=False, unique=True),
        sa.Column('new_bill_id', sa.Integer(), sa.ForeignKey('monthly_bill.id', ondelete='RESTRICT'), nullable=False, unique=True),
        sa.Column('reason', sa.String(500), nullable=False),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('user.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False))


def downgrade():
    op.drop_table('bill_change')
