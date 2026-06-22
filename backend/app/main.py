from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.core.config import settings
from app.core.response import error, success


app = FastAPI(title=settings.app_name)

cors_kwargs = {
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}

if settings.app_env == "development":
    cors_kwargs["allow_origin_regex"] = r"http://localhost:\d+"
    cors_kwargs["allow_origins"] = [
        "https://campustree.ivano.bond",
        "https://ivano.bond",
        "https://campustreex.com",
        "https://admin.campustreex.com",
    ]
else:
    cors_kwargs["allow_origins"] = [
        "https://campustree.ivano.bond",
        "https://ivano.bond",
        "https://campustreex.com",
        "https://admin.campustreex.com",
    ]

app.add_middleware(CORSMiddleware, **cors_kwargs)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and {"code", "message", "data"} <= set(
        exc.detail.keys()
    ):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content=error(message=str(exc.detail), code=exc.status_code),
    )


@app.get("/")
def health_check():
    return success({"status": "ok", "service": settings.app_name})
