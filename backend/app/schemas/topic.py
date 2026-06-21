from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TopicRead(BaseModel):
    id: int
    name: str
    post_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TopicListRead(BaseModel):
    items: list[TopicRead]
