"""Snapshot final bill amount and adjustment reason without changing legacy bills."""
from alembic import op
import sqlalchemy as sa

revision = "b35e10f97d42"
down_revision = "a24d09e86c31"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("monthly_bill", sa.Column("final_amount", sa.BigInteger(), sa.CheckConstraint("final_amount IS NULL OR final_amount >= 0", name="ck_bill_final_amount")))
    op.add_column("monthly_bill", sa.Column("adjustment_reason", sa.String(500), nullable=False, server_default=""))


def downgrade():
    with op.batch_alter_table("monthly_bill") as batch:
        batch.drop_constraint("ck_bill_final_amount", type_="check")
        batch.drop_column("adjustment_reason")
        batch.drop_column("final_amount")
