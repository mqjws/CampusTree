from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    content: str = Field(min_length=1)


class CommentUpdate(BaseModel):
    content: str = Field(min_length=1)


class CommentRead(BaseModel):
    id: int
    content: str
    author_id: int
    post_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentListRead(BaseModel):
    items: list[CommentRead]
    total: int
    page: int
    size: int
