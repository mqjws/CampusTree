from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LikeCreate(BaseModel):
    post_id: int


class LikeRead(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LikeListRead(BaseModel):
    items: list[LikeRead]
    total: int
    page: int
    size: int
