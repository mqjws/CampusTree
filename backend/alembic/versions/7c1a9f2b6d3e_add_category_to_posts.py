"""add_category_to_posts

Revision ID: 7c1a9f2b6d3e
Revises: 62b8a1c4d9e0
Create Date: 2026-06-21 00:20:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "7c1a9f2b6d3e"
down_revision: Union[str, None] = "62b8a1c4d9e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column(
            "category",
            sa.String(length=32),
            nullable=False,
            server_default="未分类",
        ),
    )


def downgrade() -> None:
    op.drop_column("posts", "category")
