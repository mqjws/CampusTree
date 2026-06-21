from typing import Annotated, Literal

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.api.deps import CurrentUserDep, OptionalCurrentUserDep, SessionDep
from app.core.response import error, success
from app.schemas.post import PostCreate, PostListRead, PostRead, PostUpdate
from app.services.post_service import (
    create_post,
    delete_post,
    get_post_by_id,
    get_posts_paginated,
    increment_post_view_count,
    update_post,
)


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
):
    items, total = get_posts_paginated(
        session,
        page=page,
        size=size,
        sort=sort,
        category=category,
        topic_id=topic_id,
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
    post = create_post(session, post_create, author_id=current_user.id)
    return success(PostRead.model_validate(post).model_dump(mode="json"))


@router.get("/{post_id}")
def read_post(
    post_id: int,
    session: SessionDep,
    current_user: OptionalCurrentUserDep,
):
    post = increment_post_view_count(
        session,
        post_id,
        current_user_id=current_user.id if current_user else None,
    )
    if post is None:
        return JSONResponse(
            status_code=404,
            content=error(message="post not found", code=404),
        )

    return success(PostRead.model_validate(post).model_dump(mode="json"))


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
