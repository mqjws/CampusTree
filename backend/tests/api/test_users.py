from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import Comment, Like, Post, User
from app.services.email_verification_service import create_email_verification_code


TEST_EMAIL_CODE = "123456"


def register_payload(
    username: str = "testuser",
    email: str = "testuser@example.com",
    password: str = "password123",
) -> dict[str, str]:
    return {
        "username": username,
        "email": email,
        "password": password,
        "email_code": TEST_EMAIL_CODE,
    }


def create_test_email_code(session: Session, email: str) -> None:
    create_email_verification_code(session, email, TEST_EMAIL_CODE)


def test_register_user_success(client: TestClient, session: Session):
    create_test_email_code(session, "testuser@example.com")

    response = client.post("/api/v1/users/register", json=register_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["username"] == "testuser"
    assert body["data"]["email"] == "testuser@example.com"
    assert "hashed_password" not in body["data"]

    user = session.exec(select(User).where(User.username == "testuser")).first()
    assert user is not None


def test_register_user_duplicate_username(client: TestClient, session: Session):
    create_test_email_code(session, "first@example.com")
    first_response = client.post(
        "/api/v1/users/register",
        json=register_payload(username="duplicate", email="first@example.com"),
    )
    create_test_email_code(session, "second@example.com")
    second_response = client.post(
        "/api/v1/users/register",
        json=register_payload(username="duplicate", email="second@example.com"),
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["message"] == "username already exists"


def test_register_user_invalid_email_code(client: TestClient):
    payload = register_payload(email="invalid-code@example.com")
    payload["email_code"] = "000000"

    response = client.post("/api/v1/users/register", json=payload)

    assert response.status_code == 400
    assert response.json()["message"] == "invalid email verification code"


def test_login_user_success(client: TestClient, session: Session):
    create_test_email_code(session, "login@example.com")
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


def test_login_user_failure(client: TestClient, session: Session):
    create_test_email_code(session, "failed@example.com")
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


def test_read_current_user_success(client: TestClient, session: Session):
    create_test_email_code(session, "me@example.com")
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


def authenticate_user(client: TestClient, session: Session, username: str, email: str) -> str:
    create_test_email_code(session, email)
    client.post(
        "/api/v1/users/register",
        json=register_payload(username=username, email=email),
    )
    login_response = client.post(
        "/api/v1/users/login",
        json={"account": username, "password": "password123"},
    )
    return login_response.json()["data"]["access_token"]


def test_read_my_posts_success(client: TestClient, session: Session):
    token = authenticate_user(client, session, "postowner", "postowner@example.com")
    user = session.exec(select(User).where(User.username == "postowner")).first()
    assert user is not None

    post = Post(title="My first post", content="post body", author_id=user.id)
    session.add(post)
    session.commit()

    response = client.get(
        "/api/v1/users/me/posts",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert len(body["data"]["items"]) == 1
    assert body["data"]["items"][0]["title"] == "My first post"


def test_read_my_comments_success(client: TestClient, session: Session):
    token = authenticate_user(client, session, "commentowner", "commentowner@example.com")
    user = session.exec(select(User).where(User.username == "commentowner")).first()
    assert user is not None

    post = Post(title="Post for comment", content="post body", author_id=user.id)
    session.add(post)
    session.commit()
    session.refresh(post)

    comment = Comment(content="My comment", author_id=user.id, post_id=post.id)
    session.add(comment)
    session.commit()

    response = client.get(
        "/api/v1/users/me/comments",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert len(body["data"]["items"]) == 1
    assert body["data"]["items"][0]["content"] == "My comment"


def test_read_my_stats_success(client: TestClient, session: Session):
    token = authenticate_user(client, session, "statsuser", "statsuser@example.com")
    user = session.exec(select(User).where(User.username == "statsuser")).first()
    assert user is not None

    post = Post(title="Stats post", content="post body", author_id=user.id)
    session.add(post)
    session.commit()
    session.refresh(post)

    comment = Comment(content="Stats comment", author_id=user.id, post_id=post.id)
    session.add(comment)
    session.commit()

    liker = User(
        username="liker",
        email="liker@example.com",
        hashed_password="hashed",
    )
    session.add(liker)
    session.commit()
    session.refresh(liker)

    like = Like(user_id=liker.id, post_id=post.id)
    session.add(like)
    session.commit()

    response = client.get(
        "/api/v1/users/me/stats",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["post_count"] == 1
    assert body["data"]["comment_count"] == 1
    assert body["data"]["like_count"] == 1


def test_update_my_password_success(client: TestClient, session: Session):
    token = authenticate_user(client, session, "passworduser", "passworduser@example.com")

    response = client.put(
        "/api/v1/users/me/password",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "old_password": "password123",
            "new_password": "newpassword123",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["message"] == "password updated"

    login_response = client.post(
        "/api/v1/users/login",
        json={"account": "passworduser", "password": "newpassword123"},
    )
    assert login_response.status_code == 200
