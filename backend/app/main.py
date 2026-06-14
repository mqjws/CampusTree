from fastapi import FastAPI

from app.core.config import settings
from app.core.response import success


app = FastAPI(title=settings.app_name)


@app.get("/")
def health_check():
    return success({"status": "ok", "service": settings.app_name})
