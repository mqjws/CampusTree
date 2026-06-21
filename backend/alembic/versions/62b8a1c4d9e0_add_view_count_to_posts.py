"""add_view_count_to_posts

Revision ID: 62b8a1c4d9e0
Revises: 31a7c0d9e4f2
Create Date: 2026-06-21 00:10:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "62b8a1c4d9e0"
down_revision: Union[str, None] = "31a7c0d9e4f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("view_count", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("posts", "view_count")
