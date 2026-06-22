from fastapi import APIRouter

from app.api.v1 import admin
from app.api.v1 import comments
from app.api.v1 import likes
from app.api.v1 import posts
from app.api.v1 import topics
from app.api.v1 import users


api_router = APIRouter()
api_router.include_router(admin.router)
api_router.include_router(comments.router)
api_router.include_router(likes.router)
api_router.include_router(posts.router)
api_router.include_router(topics.router)
api_router.include_router(users.router)
