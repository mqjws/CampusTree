from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import User


def register_payload(
    username: str = "testuser",
    email: str = "testuser@example.com",
    password: str = "password123",
) -> dict[str, str]:
    return {
        "username": username,
        "email": email,
        "password": password,
    }


def test_register_user_success(client: TestClient, session: Session):
    response = client.post("/api/v1/users/register", json=register_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["username"] == "testuser"
    assert body["data"]["email"] == "testuser@example.com"
    assert "hashed_password" not in body["data"]

    user = session.exec(select(User).where(User.username == "testuser")).first()
    assert user is not None


def test_register_user_duplicate_username(client: TestClient):
    first_response = client.post(
        "/api/v1/users/register",
        json=register_payload(username="duplicate", email="first@example.com"),
    )
    second_response = client.post(
        "/api/v1/users/register",
        json=register_payload(username="duplicate", email="second@example.com"),
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["message"] == "username already exists"


def test_login_user_success(client: TestClient):
    register_response = client.post(
        "/api/v1/users/register",
        json=register_payload(username="loginuser", email="login@example.com"),
    )
    login_response = client.post(
        "/api/v1/users/login",
        json={"account": "loginuser", "password": "password123"},
    )

    assert register_response.status_code == 200
    assert login_response.status_code == 200
    body = login_response.json()
    assert body["code"] == 200
    assert body["data"]["token_type"] == "bearer"
    assert body["data"]["access_token"]
    assert body["data"]["user"]["username"] == "loginuser"


def test_login_user_failure(client: TestClient):
    register_response = client.post(
        "/api/v1/users/register",
        json=register_payload(username="failedlogin", email="failed@example.com"),
    )
    login_response = client.post(
        "/api/v1/users/login",
        json={"account": "failedlogin", "password": "wrongpass"},
    )

    assert register_response.status_code == 200
    assert login_response.status_code == 400
    assert login_response.json()["message"] == "invalid account or password"


def test_read_current_user_success(client: TestClient):
    client.post(
        "/api/v1/users/register",
        json=register_payload(username="meuser", email="me@example.com"),
    )
    login_response = client.post(
        "/api/v1/users/login",
        json={"account": "meuser", "password": "password123"},
    )
    token = login_response.json()["data"]["access_token"]

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["username"] == "meuser"
    assert body["data"]["email"] == "me@example.com"
