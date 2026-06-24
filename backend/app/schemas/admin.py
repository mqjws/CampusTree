from pydantic import BaseModel

from app.schemas.post import PostRead
from app.schemas.post_report import PostReportRead
from app.schemas.user import UserRead


class AdminUserListRead(BaseModel):
    items: list[UserRead]
    total: int
    page: int
    size: int


class AdminUserStatusUpdate(BaseModel):
    is_active: bool


class AdminPostListRead(BaseModel):
    items: list[PostRead]
    total: int
    page: int
    size: int


class AdminReportListRead(BaseModel):
    items: list[PostReportRead]
    total: int
    page: int
    size: int
