from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.core.config import settings
from app.core.response import error, success


app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://campustree.ivano.bond",     # ← 新增
        "https://ivano.bond",                 # ← 新增
	"https://campustreex.com",             # ← 新增2
        "https://admin.campustreex.com",       # ← 新增2
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
