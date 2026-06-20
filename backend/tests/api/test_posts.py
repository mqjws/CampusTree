from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.security import create_access_token
from app.models import Comment, Post, User


def auth_headers(user: User) -> dict[str, str]:
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


def create_user(session: Session, username: str = "postuser") -> User:
    user = User(
        username=username,
        email=f"{username}@example.com",
        hashed_password="hashedpassword123",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_post(
    session: Session,
    author: User,
    title: str = "Test Post",
    content: str = "This is a test post",
) -> Post:
    post = Post(title=title, content=content, author_id=author.id)
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


def test_create_post_success(client: TestClient, session: Session):
    user = create_user(session, "createpost")

    response = client.post(
        "/api/v1/posts",
        json={"title": "New Post", "content": "New post content"},
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["title"] == "New Post"
    assert body["data"]["content"] == "New post content"
    assert body["data"]["author_id"] == user.id
    assert body["data"]["comment_count"] == 0

    post = session.exec(select(Post).where(Post.title == "New Post")).first()
    assert post is not None


def test_list_posts_success(client: TestClient, session: Session):
    user = create_user(session, "listposts")
    post_one = create_post(session, user, title="First Post")
    post_two = create_post(session, user, title="Second Post")
    create_comment(session, user, post_one, "First comment")
    create_comment(session, user, post_one, "Second comment")

    response = client.get("/api/v1/posts?page=1&size=10")

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["total"] == 2
    assert body["data"]["page"] == 1
    assert body["data"]["size"] == 10
    assert {item["id"] for item in body["data"]["items"]} == {post_one.id, post_two.id}
    counts_by_post_id = {
        item["id"]: item["comment_count"] for item in body["data"]["items"]
    }
    assert counts_by_post_id == {post_one.id: 2, post_two.id: 0}


def test_read_post_success(client: TestClient, session: Session):
    user = create_user(session, "readpost")
    post = create_post(session, user, title="Readable Post")
    create_comment(session, user, post, "Detail comment")

    response = client.get(f"/api/v1/posts/{post.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["id"] == post.id
    assert body["data"]["title"] == "Readable Post"
    assert body["data"]["comment_count"] == 1


def test_update_post_success(client: TestClient, session: Session):
    user = create_user(session, "updatepost")
    post = create_post(session, user, title="Old Title", content="Old content")

    response = client.patch(
        f"/api/v1/posts/{post.id}",
        json={"title": "Updated Title", "content": "Updated content"},
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["title"] == "Updated Title"
    assert body["data"]["content"] == "Updated content"

    session.refresh(post)
    assert post.title == "Updated Title"
    assert post.content == "Updated content"


def test_delete_post_success(client: TestClient, session: Session):
    user = create_user(session, "deletepost")
    post = create_post(session, user)
    post_id = post.id

    response = client.delete(
        f"/api/v1/posts/{post_id}",
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    assert response.json()["data"] == {"deleted": True, "post_id": post_id}
    assert session.get(Post, post_id) is None
