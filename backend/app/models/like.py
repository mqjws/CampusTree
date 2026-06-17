from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.post import Post
    from app.models.user import User


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Like(SQLModel, table=True):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("user_id", "post_id", name="uq_user_post_like"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(
        foreign_key="users.id", ondelete="CASCADE", index=True, nullable=False
    )
    post_id: int = Field(
        foreign_key="posts.id", ondelete="CASCADE", index=True, nullable=False
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    user: "User" = Relationship(back_populates="likes")
    post: "Post" = Relationship(back_populates="likes")
