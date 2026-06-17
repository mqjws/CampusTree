from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.security import create_access_token
from app.models import Comment, Post, User


def auth_headers(user: User) -> dict[str, str]:
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


def create_user(session: Session, username: str = "commentuser") -> User:
    user = User(
        username=username,
        email=f"{username}@example.com",
        hashed_password="hashedpassword123",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_post(session: Session, author: User) -> Post:
    post = Post(
        title="Commented Post",
        content="This post receives comments",
        author_id=author.id,
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def create_comment(session: Session, author: User, post: Post, content: str) -> Comment:
    comment = Comment(content=content, author_id=author.id, post_id=post.id)
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


def test_create_comment_success(client: TestClient, session: Session):
    user = create_user(session, "createcomment")
    post = create_post(session, user)

    response = client.post(
        f"/api/v1/comments/posts/{post.id}/comments",
        json={"content": "Nice post"},
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["content"] == "Nice post"
    assert body["data"]["author_id"] == user.id
    assert body["data"]["post_id"] == post.id

    comment = session.exec(select(Comment).where(Comment.content == "Nice post")).first()
    assert comment is not None


def test_list_comments_success(client: TestClient, session: Session):
    user = create_user(session, "listcomments")
    post = create_post(session, user)
    comment_one = create_comment(session, user, post, "First comment")
    comment_two = create_comment(session, user, post, "Second comment")

    response = client.get(f"/api/v1/comments/posts/{post.id}/comments?page=1&size=10")

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["total"] == 2
    assert body["data"]["page"] == 1
    assert body["data"]["size"] == 10
    assert {item["id"] for item in body["data"]["items"]} == {
        comment_one.id,
        comment_two.id,
    }


def test_delete_comment_success(client: TestClient, session: Session):
    user = create_user(session, "deletecomment")
    post = create_post(session, user)
    comment = create_comment(session, user, post, "Delete me")
    comment_id = comment.id

    response = client.delete(
        f"/api/v1/comments/{comment_id}",
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    assert response.json()["data"] == {"deleted": True, "comment_id": comment_id}
    assert session.get(Comment, comment_id) is None
