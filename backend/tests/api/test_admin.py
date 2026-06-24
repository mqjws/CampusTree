from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.security import create_access_token
from app.models import Post, PostReport, User


def auth_headers(user: User) -> dict[str, str]:
    return {"Authorization": f"Bearer {create_access_token(user.id)}"}


def create_user(session: Session, username: str, role: str = "user") -> User:
    user = User(
        username=username,
        nickname=username,
        email=f"{username}@example.com",
        hashed_password="hashedpassword123",
        role=role,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_post(session: Session, author: User, title: str = "Admin Post") -> Post:
    post = Post(title=title, content="content", author_id=author.id)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def test_admin_can_list_and_ban_users(client: TestClient, session: Session):
    admin = create_user(session, "adminuser", role="admin")
    user = create_user(session, "normaluser")

    list_response = client.get("/api/v1/admin/users", headers=auth_headers(admin))
    assert list_response.status_code == 200
    ids = {item["id"] for item in list_response.json()["data"]["items"]}
    assert {admin.id, user.id} <= ids

    ban_response = client.patch(
        f"/api/v1/admin/users/{user.id}/status",
        json={"is_active": False},
        headers=auth_headers(admin),
    )
    assert ban_response.status_code == 200
    assert ban_response.json()["data"]["is_active"] is False

    session.refresh(user)
    assert user.is_active is False


def test_admin_can_delete_any_post(client: TestClient, session: Session):
    admin = create_user(session, "postadmin", role="admin")
    author = create_user(session, "postowner")
    post = create_post(session, author, "Remove Me")
    post_id = post.id

    response = client.delete(
        f"/api/v1/admin/posts/{post_id}",
        headers=auth_headers(admin),
    )

    assert response.status_code == 200
    assert response.json()["data"] == {"deleted": True, "post_id": post_id}
    assert session.get(Post, post_id) is None


def test_admin_can_list_and_update_reports(client: TestClient, session: Session):
    admin = create_user(session, "reportadmin", role="admin")
    author = create_user(session, "reportedauthor")
    reporter = create_user(session, "reportviewer")
    post = create_post(session, author, "Reported Post")
    report = PostReport(
        post_id=post.id,
        reporter_id=reporter.id,
        reason="广告营销",
        description="广告内容",
    )
    session.add(report)
    session.commit()
    session.refresh(report)

    list_response = client.get(
        "/api/v1/admin/reports?status=pending",
        headers=auth_headers(admin),
    )
    assert list_response.status_code == 200
    assert list_response.json()["data"]["total"] == 1
    assert list_response.json()["data"]["items"][0]["post_title"] == "Reported Post"

    update_response = client.patch(
        f"/api/v1/admin/reports/{report.id}",
        json={"status": "resolved"},
        headers=auth_headers(admin),
    )
    assert update_response.status_code == 200
    assert update_response.json()["data"]["status"] == "resolved"
