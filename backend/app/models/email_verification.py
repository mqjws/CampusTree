from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class EmailVerificationCode(SQLModel, table=True):
    __tablename__ = "email_verification_codes"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, max_length=255, nullable=False)
    code_hash: str = Field(max_length=255, nullable=False)
    attempts: int = Field(default=0, nullable=False)
    expires_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    used_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
