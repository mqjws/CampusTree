from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
    allow_comments: bool = True


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)
    allow_comments: bool | None = None


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    allow_comments: bool = True
    view_count: int = 0
    comment_count: int = 0
    like_count: int = 0
    liked_by_current_user: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostListRead(BaseModel):
    items: list[PostRead]
    total: int
    page: int
    size: int
