from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, String
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.post import Post
    from app.models.user import User


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class PostReport(SQLModel, table=True):
    __tablename__ = "post_reports"

    id: int | None = Field(default=None, primary_key=True)
    post_id: int = Field(
        foreign_key="posts.id", ondelete="CASCADE", index=True, nullable=False
    )
    reporter_id: int = Field(
        foreign_key="users.id", ondelete="CASCADE", index=True, nullable=False
    )
    reason: str = Field(max_length=32, nullable=False)
    description: str = Field(default="", max_length=500, nullable=False)
    status: str = Field(
        default="pending",
        max_length=16,
        sa_column=Column(String(16), nullable=False, server_default="pending"),
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    post: "Post" = Relationship(back_populates="reports")
    reporter: "User" = Relationship(back_populates="reports")
