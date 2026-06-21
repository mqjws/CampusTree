"""add_topics_table_and_posts_topic_id

Revision ID: 3d2b7a9f4e10
Revises: 8f4e2a1d7c9b
Create Date: 2026-06-21 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "3d2b7a9f4e10"
down_revision: Union[str, None] = "8f4e2a1d7c9b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_topics_name"), "topics", ["name"], unique=True)
    op.add_column("posts", sa.Column("topic_id", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_posts_topic_id"), "posts", ["topic_id"], unique=False)
    op.create_foreign_key(
        "posts_topic_id_fkey",
        "posts",
        "topics",
        ["topic_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("posts_topic_id_fkey", "posts", type_="foreignkey")
    op.drop_index(op.f("ix_posts_topic_id"), table_name="posts")
    op.drop_column("posts", "topic_id")
    op.drop_index(op.f("ix_topics_name"), table_name="topics")
    op.drop_table("topics")
