from typing import Annotated, Literal

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from sqlmodel import func, select

from app.api.deps import AdminUserDep, SessionDep
from app.core.response import error, success
from app.models.user import User
from app.schemas.admin import (
    AdminPostListRead,
    AdminReportListRead,
    AdminUserListRead,
    AdminUserStatusUpdate,
)
from app.schemas.post import PostRead
from app.schemas.post_report import PostReportRead, PostReportUpdate
from app.schemas.sensitive_word import (
    SensitiveWordCreate,
    SensitiveWordListRead,
    SensitiveWordRead,
)
from app.services.sensitive_word_service import (
    create_word,
    delete_word,
    get_word_by_id,
    list_words,
)
from app.schemas.user import UserRead
from app.services.post_report_service import (
    get_report_by_id,
    list_reports,
    update_report_status,
)
from app.services.post_service import delete_post, get_post_by_id, get_posts_paginated

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
def read_users(
    session: SessionDep,
    _admin: AdminUserDep,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
    keyword: Annotated[str | None, Query(max_length=100)] = None,
):
    filters = []
    normalized_keyword = keyword.strip() if keyword else ""
    if normalized_keyword:
        keyword_pattern = f"%{normalized_keyword}%"
        filters.append(
            (User.username.ilike(keyword_pattern))
            | (User.email.ilike(keyword_pattern))
            | (User.nickname.ilike(keyword_pattern))
        )

    total_statement = select(func.count()).select_from(User).where(*filters)
    total = session.exec(total_statement).one()

    statement = (
        select(User)
        .where(*filters)
        .order_by(User.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
    )
    users = session.exec(statement).all()
    payload = AdminUserListRead(
        items=[UserRead.model_validate(user) for user in users],
        total=total,
        page=page,
        size=size,
    )
    return success(payload.model_dump(mode="json"))


@router.patch("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    payload: AdminUserStatusUpdate,
    session: SessionDep,
    admin: AdminUserDep,
):
    user = session.get(User, user_id)
    if user is None:
        return JSONResponse(
            status_code=404,
            content=error(message="user not found", code=404),
        )

    if user.id == admin.id and not payload.is_active:
        return JSONResponse(
            status_code=400,
            content=error(message="cannot ban yourself", code=400),
        )

    user.is_active = payload.is_active
    session.add(user)
    session.commit()
    session.refresh(user)
    return success(UserRead.model_validate(user).model_dump(mode="json"))


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    session: SessionDep,
    admin: AdminUserDep,
):
    user = session.get(User, user_id)
    if user is None:
        return JSONResponse(
            status_code=404,
            content=error(message="user not found", code=404),
        )

    if user.id == admin.id:
        return JSONResponse(
            status_code=400,
            content=error(message="cannot delete yourself", code=400),
        )

    session.delete(user)
    session.commit()
    return success({"deleted": True, "user_id": user_id})


@router.get("/posts")
def read_posts(
    session: SessionDep,
    admin: AdminUserDep,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
    sort: Literal["latest", "hot", "views", "comments", "likes"] = "latest",
    keyword: Annotated[str | None, Query(max_length=100)] = None,
):
    items, total = get_posts_paginated(
        session,
        page=page,
        size=size,
        sort=sort,
        keyword=keyword,
        current_user_id=admin.id,
    )
    payload = AdminPostListRead(
        items=[PostRead.model_validate(item) for item in items],
        total=total,
        page=page,
        size=size,
    )
    return success(payload.model_dump(mode="json"))


@router.delete("/posts/{post_id}")
def delete_any_post(
    post_id: int,
    session: SessionDep,
    _admin: AdminUserDep,
):
    post = get_post_by_id(session, post_id)
    if post is None:
        return JSONResponse(
            status_code=404,
            content=error(message="post not found", code=404),
        )

    delete_post(session, post)
    return success({"deleted": True, "post_id": post_id})


@router.get("/reports")
def read_reports(
    session: SessionDep,
    _admin: AdminUserDep,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
    status: Literal["pending", "resolved", "ignored"] | None = None,
):
    reports, total = list_reports(session, page=page, size=size, status=status)
    payload = AdminReportListRead(
        items=[PostReportRead.model_validate(report) for report in reports],
        total=total,
        page=page,
        size=size,
    )
    return success(payload.model_dump(mode="json"))


@router.patch("/reports/{report_id}")
def update_report(
    report_id: int,
    payload: PostReportUpdate,
    session: SessionDep,
    _admin: AdminUserDep,
):
    report = get_report_by_id(session, report_id)
    if report is None:
        return JSONResponse(
            status_code=404,
            content=error(message="report not found", code=404),
        )

    report = update_report_status(session, report, payload.status)
    return success(PostReportRead.model_validate(report).model_dump(mode="json"))


@router.get("/sensitive-words")
def read_sensitive_words(
    session: SessionDep,
    _admin: AdminUserDep,
    keyword: str | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
):
    items, total = list_words(session, keyword=keyword, limit=limit)
    payload = SensitiveWordListRead(
        items=[SensitiveWordRead.model_validate(item) for item in items],
        total=total,
    )
    return success(payload.model_dump(mode="json"))


@router.post("/sensitive-words")
def create_sensitive_word(
    payload: SensitiveWordCreate,
    session: SessionDep,
    _admin: AdminUserDep,
):
    word = create_word(session, payload)
    return success(SensitiveWordRead.model_validate(word).model_dump(mode="json"))


@router.delete("/sensitive-words/{word_id}")
def delete_sensitive_word(
    word_id: int,
    session: SessionDep,
    _admin: AdminUserDep,
):
    word = get_word_by_id(session, word_id)
    if word is None:
        return JSONResponse(
            status_code=404,
            content=error(message="sensitive word not found", code=404),
        )

    delete_word(session, word)
    return success({"deleted": True, "word_id": word_id})
