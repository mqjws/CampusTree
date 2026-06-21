from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from app.core.config import settings
from app.core.response import error
from app.db.session import get_session
from app.models.user import User
from app.services.user_service import get_user_by_id


SessionDep = Annotated[Session, Depends(get_session)]

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    session: SessionDep,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail=error(message="missing authorization token", code=401),
        )

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id = int(payload.get("sub"))
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=401,
            detail=error(message="token expired", code=401),
        ) from exc
    except (jwt.InvalidTokenError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=401,
            detail=error(message="invalid token", code=401),
        ) from exc

    user = get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail=error(message="invalid token", code=401),
        )

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_optional_current_user(
    session: SessionDep,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> User | None:
    if credentials is None or credentials.scheme.lower() != "bearer":
        return None

    try:
        return get_current_user(session, credentials)
    except HTTPException:
        return None


OptionalCurrentUserDep = Annotated[User | None, Depends(get_optional_current_user)]
