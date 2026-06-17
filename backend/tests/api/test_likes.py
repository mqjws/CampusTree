from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.security import create_access_token
from app.models import Like, Post, User


def auth_headers(user: User) -> dict[str, str]:
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


def create_user(session: Session, username: str) -> User:
    user = User(
        username=username,
        email=f"{username}@example.com",
        hashed_password="hashedpassword123",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_post(session: Session, author: User, title: str = "Test Post") -> Post:
    post = Post(
        title=title,
        content="This is a test post content",
        author_id=author.id,
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def get_like(session: Session, user_id: int, post_id: int) -> Like | None:
    statement = select(Like).where(Like.user_id == user_id, Like.post_id == post_id)
    return session.exec(statement).first()


def test_like_post_success(client: TestClient, session: Session):
    user = create_user(session, "likeuser")
    post = create_post(session, user)

    response = client.post(
        f"/api/v1/posts/{post.id}/like",
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["user_id"] == user.id
    assert body["data"]["post_id"] == post.id
    assert get_like(session, user.id, post.id) is not None


def test_like_post_duplicate(client: TestClient, session: Session):
    user = create_user(session, "duplicateuser")
    post = create_post(session, user)

    first_response = client.post(
        f"/api/v1/posts/{post.id}/like",
        headers=auth_headers(user),
    )
    second_response = client.post(
        f"/api/v1/posts/{post.id}/like",
        headers=auth_headers(user),
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["message"] == "post already liked"

    likes = session.exec(
        select(Like).where(Like.user_id == user.id, Like.post_id == post.id)
    ).all()
    assert len(likes) == 1


def test_unlike_post_success(client: TestClient, session: Session):
    user = create_user(session, "unlikeuser")
    post = create_post(session, user)

    like_response = client.post(
        f"/api/v1/posts/{post.id}/like",
        headers=auth_headers(user),
    )
    unlike_response = client.delete(
        f"/api/v1/posts/{post.id}/like",
        headers=auth_headers(user),
    )

    assert like_response.status_code == 200
    assert unlike_response.status_code == 200
    assert unlike_response.json()["data"] == {"deleted": True, "post_id": post.id}
    assert get_like(session, user.id, post.id) is None


def test_unlike_post_not_liked(client: TestClient, session: Session):
    user = create_user(session, "notlikeduser")
    post = create_post(session, user)

    response = client.delete(
        f"/api/v1/posts/{post.id}/like",
        headers=auth_headers(user),
    )

    assert response.status_code == 400
    assert response.json()["message"] == "post not liked"


def test_like_deleted_when_user_is_deleted(client: TestClient, session: Session):
    author = create_user(session, "cascadeauthor")
    liker = create_user(session, "cascadeliker")
    post = create_post(session, author)

    response = client.post(
        f"/api/v1/posts/{post.id}/like",
        headers=auth_headers(liker),
    )
    like_id = response.json()["data"]["id"]

    session.delete(liker)
    session.commit()

    assert response.status_code == 200
    assert session.get(Post, post.id) is not None
    assert session.get(Like, like_id) is None


def test_like_deleted_when_post_is_deleted(client: TestClient, session: Session):
    author = create_user(session, "postcascadeauthor")
    liker = create_user(session, "postcascadeliker")
    post = create_post(session, author)

    response = client.post(
        f"/api/v1/posts/{post.id}/like",
        headers=auth_headers(liker),
    )
    like_id = response.json()["data"]["id"]

    session.delete(post)
    session.commit()

    assert response.status_code == 200
    assert session.get(Like, like_id) is None
