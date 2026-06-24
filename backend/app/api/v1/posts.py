from typing import Annotated, Literal

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.api.deps import CurrentUserDep, OptionalCurrentUserDep, SessionDep
from app.core.response import error, success
from app.schemas.post import PostCreate, PostListRead, PostRead, PostUpdate
from app.schemas.post_report import PostReportCreate, PostReportRead
from app.services.post_report_service import (
    DuplicatePendingReportError,
    create_post_report,
)
from app.services.post_service import (
    create_post,
    delete_post,
    get_post_by_id,
    get_posts_paginated,
    increment_post_view_count,
    update_post,
)
from app.services.sensitive_word_service import check_sensitive_words


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("")
def list_posts(
    session: SessionDep,
    current_user: OptionalCurrentUserDep,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
    sort: Literal["latest", "hot", "views", "comments", "likes"] = "latest",
    category: str | None = None,
    topic_id: int | None = None,
    keyword: Annotated[str | None, Query(max_length=100)] = None,
):
    items, total = get_posts_paginated(
        session,
        page=page,
        size=size,
        sort=sort,
        category=category,
        topic_id=topic_id,
        keyword=keyword,
        current_user_id=current_user.id if current_user else None,
    )
    result = PostListRead(
        items=[PostRead.model_validate(item) for item in items],
        total=total,
        page=page,
        size=size,
    )
    return success(result.model_dump(mode="json"))


@router.post("")
def create_post_api(
    post_create: PostCreate,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    matched = check_sensitive_words(session, post_create.content)
    if matched:
        return JSONResponse(
            status_code=400,
            content=error(
                message=f"内容包含敏感词：{', '.join(matched)}", code=400
            ),
        )

    post = create_post(session, post_create, author_id=current_user.id)
    return success(PostRead.model_validate(post).model_dump(mode="json"))


@router.get("/{post_id}")
def read_post(
    post_id: int,
    session: SessionDep,
    current_user: OptionalCurrentUserDep,
):
    post = get_post_by_id(
        session,
        post_id,
        current_user_id=current_user.id if current_user else None,
    )
    if post is None:
        return JSONResponse(
            status_code=404,
            content=error(message="post not found", code=404),
        )

    if post.registered_only and current_user is None:
        return JSONResponse(
            status_code=401,
            content=error(message="login required to view this post", code=401),
        )

    post = increment_post_view_count(
        session,
        post_id,
        current_user_id=current_user.id if current_user else None,
    )

    return success(PostRead.model_validate(post).model_dump(mode="json"))


@router.post("/{post_id}/reports")
def report_post_api(
    post_id: int,
    payload: PostReportCreate,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    post = get_post_by_id(session, post_id, current_user_id=current_user.id)
    if post is None:
        return JSONResponse(
            status_code=404,
            content=error(message="post not found", code=404),
        )

    try:
        report = create_post_report(
            session,
            payload,
            post_id=post_id,
            reporter_id=current_user.id,
        )
    except DuplicatePendingReportError:
        return JSONResponse(
            status_code=400,
            content=error(message="report already submitted", code=400),
        )

    return success(PostReportRead.model_validate(report).model_dump(mode="json"))


@router.patch("/{post_id}")
def update_post_api(
    post_id: int,
    post_update: PostUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    post = get_post_by_id(session, post_id)
    if post is None:
        return JSONResponse(
            status_code=404,
            content=error(message="post not found", code=404),
        )

    if post.author_id != current_user.id:
        return JSONResponse(
            status_code=403,
            content=error(message="forbidden", code=403),
        )

    post = update_post(session, post, post_update)
    return success(PostRead.model_validate(post).model_dump(mode="json"))


@router.delete("/{post_id}")
def delete_post_api(
    post_id: int,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    post = get_post_by_id(session, post_id)
    if post is None:
        return JSONResponse(
            status_code=404,
            content=error(message="post not found", code=404),
        )

    if post.author_id != current_user.id:
        return JSONResponse(
            status_code=403,
            content=error(message="forbidden", code=403),
        )

    delete_post(session, post)
    return success({"deleted": True, "post_id": post_id})
