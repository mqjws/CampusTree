from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SensitiveWord(SQLModel, table=True):
    __tablename__ = "sensitive_words"

    id: int | None = Field(default=None, primary_key=True)
    word: str = Field(index=True, unique=True, max_length=50, nullable=False)
    created_at: datetime = Field(default_factory=utc_now, nullable=False)
