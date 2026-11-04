"""One photo per meter reading; keep a fallback while replacement is processed."""
from alembic import op
import sqlalchemy as sa

revision = "a24d09e86c31"
down_revision = "f13a98c52b70"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("photo", sa.Column("previous_token", sa.String(32)))
    connection = op.get_bind()
    # Preserve the newest ready image, or newest job if none is ready.
    rows = connection.execute(sa.text(
        "SELECT id, reading_id, status FROM photo WHERE reading_id IS NOT NULL ORDER BY id DESC"
    )).mappings().all()
    keep = {}
    for row in rows:
        current = keep.get(row["reading_id"])
        if current is None or (current["status"] != "ready" and row["status"] == "ready"):
            keep[row["reading_id"]] = row
    for row in rows:
        if row["id"] != keep[row["reading_id"]]["id"]:
            connection.execute(sa.text("DELETE FROM photo WHERE id = :id"), {"id": row["id"]})
    op.create_index("uq_photo_reading", "photo", ["reading_id"], unique=True)


def downgrade():
    op.drop_index("uq_photo_reading", table_name="photo")
    with op.batch_alter_table("photo") as batch:
        batch.drop_column("previous_token")
