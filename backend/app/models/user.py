from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, String
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.like import Like
    from app.models.post import Post
    from app.models.post_report import PostReport


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50, nullable=False)
    nickname: str = Field(default="", max_length=50, nullable=False)
    email: str = Field(index=True, unique=True, max_length=255, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    avatar_url: str | None = Field(default=None, max_length=500)
    role: str = Field(
        default="user",
        max_length=16,
        sa_column=Column(String(16), nullable=False, server_default="user"),
    )
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    posts: list["Post"] = Relationship(back_populates="author", cascade_delete=True)
    comments: list["Comment"] = Relationship(back_populates="author", cascade_delete=True)
    likes: list["Like"] = Relationship(back_populates="user", cascade_delete=True)
    reports: list["PostReport"] = Relationship(back_populates="reporter", cascade_delete=True)
