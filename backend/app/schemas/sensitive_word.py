from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SensitiveWordCreate(BaseModel):
    word: str = Field(min_length=1, max_length=50)


class SensitiveWordRead(BaseModel):
    id: int
    word: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SensitiveWordListRead(BaseModel):
    items: list[SensitiveWordRead]
    total: int
