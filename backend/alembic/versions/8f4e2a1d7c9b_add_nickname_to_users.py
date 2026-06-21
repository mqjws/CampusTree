"""add_nickname_to_users

Revision ID: 8f4e2a1d7c9b
Revises: 7c1a9f2b6d3e
Create Date: 2026-06-21 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "8f4e2a1d7c9b"
down_revision: Union[str, None] = "7c1a9f2b6d3e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("nickname", sa.String(length=50), nullable=True))
    op.execute("UPDATE users SET nickname = username WHERE nickname IS NULL")
    op.alter_column("users", "nickname", nullable=False)


def downgrade() -> None:
    op.drop_column("users", "nickname")
