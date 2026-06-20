from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    comment_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostListRead(BaseModel):
    items: list[PostRead]
    total: int
    page: int
    size: int
