from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.deps import CurrentUserDep, SessionDep
from app.core.response import error, success
from app.core.security import create_access_token, verify_password
from app.schemas.user import UserCreate, UserLogin, UserLoginRead, UserRead
from app.services.user_service import (
    create_user,
    get_user_by_account,
    get_user_by_email,
    get_user_by_username,
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

    user = create_user(session, user_create)
    return success(UserRead.model_validate(user).model_dump(mode="json"))


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
