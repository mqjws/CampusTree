from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.post import Post
    from app.models.user import User


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(nullable=False)
    author_id: int = Field(
        foreign_key="users.id", ondelete="CASCADE", index=True, nullable=False
    )
    post_id: int = Field(
        foreign_key="posts.id", ondelete="CASCADE", index=True, nullable=False
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    author: "User" = Relationship(back_populates="comments")
    post: "Post" = Relationship(back_populates="comments")
