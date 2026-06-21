"""add_allow_comments_to_posts

Revision ID: 31a7c0d9e4f2
Revises: d6a4f82c9b10
Create Date: 2026-06-21 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "31a7c0d9e4f2"
down_revision: Union[str, None] = "d6a4f82c9b10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column(
            "allow_comments",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )


def downgrade() -> None:
    op.drop_column("posts", "allow_comments")
