"""add_ondelete_cascade_to_relationship_fks

Revision ID: f2c8d9e1a7b3
Revises: a83709e32167
Create Date: 2026-06-17 17:34:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "f2c8d9e1a7b3"
down_revision: Union[str, None] = "a83709e32167"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("likes_post_id_fkey", "likes", type_="foreignkey")
    op.drop_constraint("likes_user_id_fkey", "likes", type_="foreignkey")
    op.drop_constraint("comments_post_id_fkey", "comments", type_="foreignkey")
    op.drop_constraint("comments_author_id_fkey", "comments", type_="foreignkey")
    op.drop_constraint("posts_author_id_fkey", "posts", type_="foreignkey")

    op.create_foreign_key(
        "posts_author_id_fkey",
        "posts",
        "users",
        ["author_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "comments_author_id_fkey",
        "comments",
        "users",
        ["author_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "comments_post_id_fkey",
        "comments",
        "posts",
        ["post_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "likes_user_id_fkey",
        "likes",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "likes_post_id_fkey",
        "likes",
        "posts",
        ["post_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("likes_post_id_fkey", "likes", type_="foreignkey")
    op.drop_constraint("likes_user_id_fkey", "likes", type_="foreignkey")
    op.drop_constraint("comments_post_id_fkey", "comments", type_="foreignkey")
    op.drop_constraint("comments_author_id_fkey", "comments", type_="foreignkey")
    op.drop_constraint("posts_author_id_fkey", "posts", type_="foreignkey")

    op.create_foreign_key(
        "posts_author_id_fkey",
        "posts",
        "users",
        ["author_id"],
        ["id"],
    )
    op.create_foreign_key(
        "comments_author_id_fkey",
        "comments",
        "users",
        ["author_id"],
        ["id"],
    )
    op.create_foreign_key(
        "comments_post_id_fkey",
        "comments",
        "posts",
        ["post_id"],
        ["id"],
    )
    op.create_foreign_key(
        "likes_user_id_fkey",
        "likes",
        "users",
        ["user_id"],
        ["id"],
    )
    op.create_foreign_key(
        "likes_post_id_fkey",
        "likes",
        "posts",
        ["post_id"],
        ["id"],
    )
