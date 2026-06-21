from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.like import Like
    from app.models.user import User


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=100, nullable=False)
    content: str = Field(nullable=False)
    category: str = Field(default="未分类", max_length=32, nullable=False)
    allow_comments: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False, server_default="true"),
    )
    view_count: int = Field(default=0, ge=0, nullable=False)
    author_id: int = Field(
        foreign_key="users.id", ondelete="CASCADE", index=True, nullable=False
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    author: "User" = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post", cascade_delete=True)
    likes: list["Like"] = Relationship(back_populates="post", cascade_delete=True)
