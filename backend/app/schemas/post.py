from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(default="", max_length=2000)
    category: str = Field(default="未分类", min_length=1, max_length=32)
    topic_name: str | None = Field(default=None, max_length=50)
    allow_comments: bool = True
    registered_only: bool = False


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, max_length=2000)
    category: str | None = Field(default=None, min_length=1, max_length=32)
    allow_comments: bool | None = None
    registered_only: bool | None = None


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    category: str = "未分类"
    author_id: int
    author_nickname: str
    topic_id: int | None = None
    topic_name: str | None = None
    allow_comments: bool = True
    registered_only: bool = False
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
