from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.deps import CurrentUserDep, SessionDep
from app.core.response import error, success
from app.core.security import create_access_token, verify_password
from app.schemas.comment import CommentRead
from app.schemas.post import PostRead
from app.schemas.user import (
    EmailCodeCreate,
    UserCommentListRead,
    UserCreate,
    UserLogin,
    UserLoginRead,
    UserPasswordUpdate,
    UserProfileUpdate,
    UserPostListRead,
    UserRead,
    UserStatsRead,
)
from app.services.user_service import (
    create_user,
    get_comments_by_user_id,
    get_posts_by_user_id,
    get_user_by_account,
    get_user_by_email,
    get_user_by_username,
    get_user_stats,
    update_user_password,
    update_user_profile,
)
from app.services.email_service import EmailConfigError, send_register_code_email
from app.services.email_verification_service import (
    EmailCodeCooldownError,
    EmailCodeInvalidError,
    create_email_verification_code,
    delete_latest_unused_email_code,
    verify_email_code,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
def register_user(user_create: UserCreate, session: SessionDep):
    if get_user_by_username(session, user_create.username):
        return JSONResponse(
            status_code=400,
            content=error(message="username already exists", code=400),
        )

    if get_user_by_email(session, str(user_create.email)):
        return JSONResponse(
            status_code=400,
            content=error(message="email already exists", code=400),
        )

    try:
        verify_email_code(session, str(user_create.email), user_create.email_code)
    except EmailCodeInvalidError:
        return JSONResponse(
            status_code=400,
            content=error(message="invalid email verification code", code=400),
        )

    user = create_user(session, user_create)
    return success(UserRead.model_validate(user).model_dump(mode="json"))


@router.post("/email-code")
def send_email_code(payload: EmailCodeCreate, session: SessionDep):
    if get_user_by_email(session, str(payload.email)):
        return JSONResponse(
            status_code=400,
            content=error(message="email already exists", code=400),
        )

    try:
        code = create_email_verification_code(session, str(payload.email))
    except EmailCodeCooldownError:
        return JSONResponse(
            status_code=429,
            content=error(message="email code sent too frequently", code=429),
        )

    try:
        send_register_code_email(str(payload.email), code)
    except EmailConfigError:
        delete_latest_unused_email_code(session, str(payload.email))
        return JSONResponse(
            status_code=500,
            content=error(message="email service is not configured", code=500),
        )
    except Exception:
        delete_latest_unused_email_code(session, str(payload.email))
        return JSONResponse(
            status_code=500,
            content=error(message="email code send failed", code=500),
        )

    return success({"sent": True}, message="email code sent")


@router.post("/login")
def login_user(user_login: UserLogin, session: SessionDep):
    user = get_user_by_account(session, user_login.account)
    if not user or not verify_password(user_login.password, user.hashed_password):
        return JSONResponse(
            status_code=400,
            content=error(message="invalid account or password", code=400),
        )

    user_read = UserRead.model_validate(user)
    login_read = UserLoginRead(
        access_token=create_access_token(user.id),
        user=user_read,
    )
    return success(login_read.model_dump(mode="json"))


@router.get("/me")
def read_current_user(current_user: CurrentUserDep):
    return success(UserRead.model_validate(current_user).model_dump(mode="json"))


@router.put("/me/profile")
def update_my_profile(
    payload: UserProfileUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    user = update_user_profile(session, current_user, payload.nickname)
    return success(UserRead.model_validate(user).model_dump(mode="json"))


@router.get("/me/posts")
def read_my_posts(session: SessionDep, current_user: CurrentUserDep):
    posts = get_posts_by_user_id(session, current_user.id)
    payload = UserPostListRead(items=[PostRead.model_validate(post) for post in posts])
    return success(payload.model_dump(mode="json"))


@router.get("/me/comments")
def read_my_comments(session: SessionDep, current_user: CurrentUserDep):
    comments = get_comments_by_user_id(session, current_user.id)
    payload = UserCommentListRead(
        items=[CommentRead.model_validate(comment) for comment in comments]
    )
    return success(payload.model_dump(mode="json"))


@router.get("/me/stats")
def read_my_stats(session: SessionDep, current_user: CurrentUserDep):
    stats = get_user_stats(session, current_user.id)
    payload = UserStatsRead(**stats)
    return success(payload.model_dump(mode="json"))


@router.put("/me/password")
def update_my_password(
    payload: UserPasswordUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    updated, message = update_user_password(
        session, current_user, payload.old_password, payload.new_password
    )
    if not updated:
        return JSONResponse(
            status_code=400,
            content=error(message=message, code=400),
        )

    return success({"updated": True}, message=message)
