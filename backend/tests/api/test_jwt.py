from datetime import datetime, timedelta, timezone

import jwt
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.models import User


def create_user(session: Session, username: str = "jwtuser") -> User:
    user = User(
        username=username,
        email=f"{username}@example.com",
        hashed_password="hashedpassword123",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_missing_token_returns_401(client: TestClient):
    response = client.get("/api/v1/users/me")

    assert response.status_code == 401
    assert response.json()["message"] == "missing authorization token"


def test_invalid_token_returns_401(client: TestClient):
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid.token"},
    )

    assert response.status_code == 401
    assert response.json()["message"] == "invalid token"


def test_expired_token_returns_401(client: TestClient, session: Session):
    user = create_user(session, "expiredjwt")
    token = jwt.encode(
        {
            "sub": str(user.id),
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.json()["message"] == "token expired"


def test_valid_token_returns_current_user(client: TestClient, session: Session):
    user = create_user(session, "validjwt")
    token = create_access_token(user.id)

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["id"] == user.id
    assert body["data"]["username"] == "validjwt"
