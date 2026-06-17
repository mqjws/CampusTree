from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.api.deps import CurrentUserDep, SessionDep
from app.core.response import error, success
from app.schemas.comment import CommentCreate, CommentListRead, CommentRead, CommentUpdate
from app.services.comment_service import (
    create_comment,
    delete_comment,
    get_comment_by_id,
    get_comments_by_post_paginated,
    update_comment,
)
from app.services.post_service import get_post_by_id


router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/posts/{post_id}/comments")
def create_comment_api(
    post_id: int,
    comment_create: CommentCreate,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    # 验证帖子是否存在
    post = get_post_by_id(session, post_id)
    if post is None:
        return JSONResponse(
            status_code=404,
            content=error(message="post not found", code=404),
        )

    comment = create_comment(
        session, comment_create, author_id=current_user.id, post_id=post_id
    )
    return success(CommentRead.model_validate(comment).model_dump(mode="json"))


@router.get("/posts/{post_id}/comments")
def list_comments_by_post(
    post_id: int,
    session: SessionDep,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
):
    # 验证帖子是否存在
    post = get_post_by_id(session, post_id)
    if post is None:
        return JSONResponse(
            status_code=404,
            content=error(message="post not found", code=404),
        )

    items, total = get_comments_by_post_paginated(
        session, post_id=post_id, page=page, size=size
    )
    result = CommentListRead(
        items=[CommentRead.model_validate(item) for item in items],
        total=total,
        page=page,
        size=size,
    )
    return success(result.model_dump(mode="json"))


@router.get("/{comment_id}")
def read_comment(comment_id: int, session: SessionDep):
    comment = get_comment_by_id(session, comment_id)
    if comment is None:
        return JSONResponse(
            status_code=404,
            content=error(message="comment not found", code=404),
        )

    return success(CommentRead.model_validate(comment).model_dump(mode="json"))


@router.patch("/{comment_id}")
def update_comment_api(
    comment_id: int,
    comment_update: CommentUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    comment = get_comment_by_id(session, comment_id)
    if comment is None:
        return JSONResponse(
            status_code=404,
            content=error(message="comment not found", code=404),
        )

    if comment.author_id != current_user.id:
        return JSONResponse(
            status_code=403,
            content=error(message="forbidden", code=403),
        )

    comment = update_comment(session, comment, comment_update)
    return success(CommentRead.model_validate(comment).model_dump(mode="json"))


@router.delete("/{comment_id}")
def delete_comment_api(
    comment_id: int,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    comment = get_comment_by_id(session, comment_id)
    if comment is None:
        return JSONResponse(
            status_code=404,
            content=error(message="comment not found", code=404),
        )

    if comment.author_id != current_user.id:
        return JSONResponse(
            status_code=403,
            content=error(message="forbidden", code=403),
        )

    delete_comment(session, comment)
    return success({"deleted": True, "comment_id": comment_id})
