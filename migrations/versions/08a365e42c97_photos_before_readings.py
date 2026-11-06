"""Allow a meter photo to belong to a room/month before reading entry."""
from alembic import op
import sqlalchemy as sa

revision = "08a365e42c97"
down_revision = "f79254d31b86"
branch_labels = None
depends_on = None

OLD_OWNER = "(tenancy_id IS NOT NULL AND reading_id IS NULL) OR (tenancy_id IS NULL AND reading_id IS NOT NULL)"
NEW_OWNER = "(tenancy_id IS NOT NULL AND reading_id IS NULL AND room_id IS NULL AND period IS NULL) OR (tenancy_id IS NULL AND reading_id IS NOT NULL AND room_id IS NULL AND period IS NULL) OR (tenancy_id IS NULL AND reading_id IS NULL AND room_id IS NOT NULL AND period IS NOT NULL)"


def upgrade():
    with op.batch_alter_table("photo") as batch:
        batch.add_column(sa.Column("room_id", sa.Integer(), nullable=True))
        batch.add_column(sa.Column("period", sa.String(7), nullable=True))
        batch.create_foreign_key("fk_photo_room", "room", ["room_id"], ["id"], ondelete="RESTRICT")
        batch.drop_constraint("ck_photo_owner", type_="check")
        batch.create_check_constraint("ck_photo_owner", NEW_OWNER)
        batch.create_index("uq_photo_room_period", ["room_id", "period"], unique=True)


def downgrade():
    if op.get_bind().execute(sa.text("SELECT id FROM photo WHERE room_id IS NOT NULL LIMIT 1")).first():
        raise RuntimeError("Attach room/month photos to readings before downgrading; no photos were deleted.")
    with op.batch_alter_table("photo") as batch:
        batch.drop_index("uq_photo_room_period")
        batch.drop_constraint("ck_photo_owner", type_="check")
        batch.drop_constraint("fk_photo_room", type_="foreignkey")
        batch.drop_column("period")
        batch.drop_column("room_id")
        batch.create_check_constraint("ck_photo_owner", OLD_OWNER)
