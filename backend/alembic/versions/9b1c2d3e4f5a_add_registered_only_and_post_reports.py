"""add_registered_only_and_post_reports

Revision ID: 9b1c2d3e4f5a
Revises: 5f6g7h8i9j0k
Create Date: 2026-06-24 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9b1c2d3e4f5a"
down_revision: Union[str, None] = "5f6g7h8i9j0k"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column(
            "registered_only",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.create_table(
        "post_reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("reporter_id", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(length=32), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=False),
        sa.Column(
            "status",
            sa.String(length=16),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["reporter_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_post_reports_post_id", "post_reports", ["post_id"])
    op.create_index("ix_post_reports_reporter_id", "post_reports", ["reporter_id"])
    op.create_index("ix_post_reports_status", "post_reports", ["status"])


def downgrade() -> None:
    op.drop_index("ix_post_reports_status", table_name="post_reports")
    op.drop_index("ix_post_reports_reporter_id", table_name="post_reports")
    op.drop_index("ix_post_reports_post_id", table_name="post_reports")
    op.drop_table("post_reports")
    op.drop_column("posts", "registered_only")
