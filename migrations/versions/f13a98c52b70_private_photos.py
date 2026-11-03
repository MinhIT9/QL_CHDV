"""Private contract and meter photos with persistent compression queue."""
from alembic import op
import sqlalchemy as sa

revision = "f13a98c52b70"
down_revision = "41eb1b88b816"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "photo",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("token", sa.String(32), nullable=False, unique=True),
        sa.Column("tenancy_id", sa.Integer(), sa.ForeignKey("tenancy.id", ondelete="RESTRICT")),
        sa.Column("reading_id", sa.Integer(), sa.ForeignKey("electricity_reading.id", ondelete="RESTRICT")),
        sa.Column("status", sa.String(16), nullable=False),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("user.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("(tenancy_id IS NOT NULL AND reading_id IS NULL) OR (tenancy_id IS NULL AND reading_id IS NOT NULL)", name="ck_photo_owner"),
        sa.CheckConstraint("status IN ('pending', 'ready', 'failed')", name="ck_photo_status"),
    )


def downgrade():
    op.drop_table("photo")
