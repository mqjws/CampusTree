from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.comment import CommentRead
from app.schemas.post import PostRead


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(
        min_length=5,
        max_length=255,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )
    password: str = Field(min_length=5, max_length=72)
    email_code: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")


class EmailCodeCreate(BaseModel):
    email: str = Field(
        min_length=5,
        max_length=255,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )


class UserLogin(BaseModel):
    account: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=5, max_length=72)


class UserPasswordUpdate(BaseModel):
    old_password: str = Field(min_length=5, max_length=72)
    new_password: str = Field(min_length=5, max_length=72)


class UserProfileUpdate(BaseModel):
    nickname: str = Field(min_length=1, max_length=50)

    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, value: str) -> str:
        nickname = value.strip()
        if not nickname:
            raise ValueError("nickname must not be blank")
        return nickname


class UserRead(BaseModel):
    id: int
    username: str
    nickname: str
    email: str
    avatar_url: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLoginRead(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class UserPostListRead(BaseModel):
    items: list[PostRead]


class UserCommentListRead(BaseModel):
    items: list[CommentRead]


class UserStatsRead(BaseModel):
    post_count: int
    comment_count: int
    like_count: int
