"""create sensitive_words table

Revision ID: 5f6g7h8i9j0k
Revises: 4e5f6a7b8c9d
Create Date: 2026-06-22 20:01:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "5f6g7h8i9j0k"
down_revision: Union[str, None] = "4e5f6a7b8c9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sensitive_words",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "word",
            sqlmodel.sql.sqltypes.AutoString(length=50),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_sensitive_words_word"),
        "sensitive_words",
        ["word"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_sensitive_words_word"), table_name="sensitive_words")
    op.drop_table("sensitive_words")
