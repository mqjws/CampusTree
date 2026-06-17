from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.deps import CurrentUserDep, SessionDep
from app.core.response import error, success
from app.schemas.like import LikeRead
from app.services.like_service import (
    LikeAlreadyExistsError,
    LikeNotFoundError,
    like_post,
    unlike_post,
)
from app.services.post_service import get_post_by_id


router = APIRouter(prefix="/posts", tags=["likes"])


@router.post("/{post_id}/like")
def like_post_api(
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

    try:
        like = like_post(session, user_id=current_user.id, post_id=post_id)
    except LikeAlreadyExistsError:
        return JSONResponse(
            status_code=400,
            content=error(message="post already liked", code=400),
        )

    return success(LikeRead.model_validate(like).model_dump(mode="json"))


@router.delete("/{post_id}/like")
def unlike_post_api(
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

    try:
        unlike_post(session, user_id=current_user.id, post_id=post_id)
    except LikeNotFoundError:
        return JSONResponse(
            status_code=400,
            content=error(message="post not liked", code=400),
        )

    return success({"deleted": True, "post_id": post_id})
