from fastapi import APIRouter

from app.api.v1 import posts
from app.api.v1 import users


api_router = APIRouter()
api_router.include_router(posts.router)
api_router.include_router(users.router)
