from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ReportStatus = Literal["pending", "resolved", "ignored"]


class PostReportCreate(BaseModel):
    reason: str = Field(min_length=1, max_length=32)
    description: str = Field(default="", max_length=500)


class PostReportUpdate(BaseModel):
    status: ReportStatus


class PostReportRead(BaseModel):
    id: int
    post_id: int
    post_title: str | None = None
    reporter_id: int
    reporter_username: str | None = None
    reason: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostReportListRead(BaseModel):
    items: list[PostReportRead]
    total: int
    page: int
    size: int
