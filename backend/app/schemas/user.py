from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(
        min_length=5,
        max_length=255,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )
    password: str = Field(min_length=6, max_length=72)


class UserLogin(BaseModel):
    account: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=6, max_length=72)


class UserRead(BaseModel):
    id: int
    username: str
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
