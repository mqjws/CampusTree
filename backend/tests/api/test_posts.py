from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.security import create_access_token
from app.models import Comment, Like, Post, User


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
    view_count: int = 0,
    category: str = "未分类",
    registered_only: bool = False,
) -> Post:
    post = Post(
        title=title,
        content=content,
        category=category,
        author_id=author.id,
        view_count=view_count,
        registered_only=registered_only,
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


def create_like(session: Session, user: User, post: Post) -> Like:
    like = Like(user_id=user.id, post_id=post.id)
    session.add(like)
    session.commit()
    session.refresh(like)
    return like


def test_create_post_success(client: TestClient, session: Session):
    user = create_user(session, "createpost")

    response = client.post(
        "/api/v1/posts",
        json={"title": "New Post", "content": "New post content", "category": "学习"},
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["title"] == "New Post"
    assert body["data"]["content"] == "New post content"
    assert body["data"]["category"] == "学习"
    assert body["data"]["author_id"] == user.id
    assert body["data"]["allow_comments"] is True
    assert body["data"]["registered_only"] is False
    assert body["data"]["view_count"] == 0
    assert body["data"]["comment_count"] == 0
    assert body["data"]["like_count"] == 0

    post = session.exec(select(Post).where(Post.title == "New Post")).first()
    assert post is not None
    assert post.category == "学习"


def test_create_post_allows_empty_content(client: TestClient, session: Session):
    user = create_user(session, "emptycontent")

    response = client.post(
        "/api/v1/posts",
        json={"title": "Empty Content", "content": ""},
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["title"] == "Empty Content"
    assert body["data"]["content"] == ""


def test_create_post_can_disable_comments(client: TestClient, session: Session):
    user = create_user(session, "disablepostcomments")

    response = client.post(
        "/api/v1/posts",
        json={
            "title": "No Comments",
            "content": "New post content",
            "allow_comments": False,
        },
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["allow_comments"] is False

    post = session.exec(select(Post).where(Post.title == "No Comments")).first()
    assert post is not None
    assert post.allow_comments is False


def test_create_post_can_be_registered_only(client: TestClient, session: Session):
    user = create_user(session, "registeredonlyauthor")

    response = client.post(
        "/api/v1/posts",
        json={
            "title": "Members Only",
            "content": "Only logged in users can see this",
            "registered_only": True,
        },
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["registered_only"] is True

    post = session.exec(select(Post).where(Post.title == "Members Only")).first()
    assert post is not None
    assert post.registered_only is True


def test_list_posts_success(client: TestClient, session: Session):
    user = create_user(session, "listposts")
    post_one = create_post(session, user, title="First Post")
    post_two = create_post(session, user, title="Second Post")
    create_comment(session, user, post_one, "First comment")
    create_comment(session, user, post_one, "Second comment")
    create_like(session, user, post_one)
    create_like(session, user, post_two)

    response = client.get("/api/v1/posts?page=1&size=10")

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["total"] == 2
    assert body["data"]["page"] == 1
    assert body["data"]["size"] == 10
    assert {item["id"] for item in body["data"]["items"]} == {post_one.id, post_two.id}
    counts_by_post_id = {
        item["id"]: (item["comment_count"], item["like_count"])
        for item in body["data"]["items"]
    }
    assert counts_by_post_id == {post_one.id: (2, 1), post_two.id: (0, 1)}


def test_list_posts_hides_registered_only_from_guests(
    client: TestClient, session: Session
):
    user = create_user(session, "visibilityauthor")
    public_post = create_post(session, user, title="Public Post")
    private_post = create_post(
        session,
        user,
        title="Registered Only Post",
        registered_only=True,
    )

    guest_response = client.get("/api/v1/posts?page=1&size=10")
    assert guest_response.status_code == 200
    guest_body = guest_response.json()
    assert guest_body["data"]["total"] == 1
    assert [item["id"] for item in guest_body["data"]["items"]] == [public_post.id]

    auth_response = client.get(
        "/api/v1/posts?page=1&size=10",
        headers=auth_headers(user),
    )
    assert auth_response.status_code == 200
    auth_ids = {item["id"] for item in auth_response.json()["data"]["items"]}
    assert auth_ids == {public_post.id, private_post.id}


def test_list_posts_can_filter_by_category(client: TestClient, session: Session):
    user = create_user(session, "categoryposts")
    study_post = create_post(session, user, title="Study Post", category="学习")
    create_post(session, user, title="Food Post", category="美食")

    response = client.get("/api/v1/posts?page=1&size=10&category=学习")

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["total"] == 1
    assert [item["id"] for item in body["data"]["items"]] == [study_post.id]
    assert body["data"]["items"][0]["category"] == "学习"


def test_list_posts_can_search_by_keyword(client: TestClient, session: Session):
    user = create_user(session, "searchposts")
    title_match = create_post(session, user, title="考研数学资料")
    content_match = create_post(
        session,
        user,
        title="晚自习",
        content="图书馆座位预约经验分享",
    )
    create_post(session, user, title="食堂测评", content="今天二楼窗口不错")

    response = client.get("/api/v1/posts?page=1&size=10&keyword=图书馆")

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["total"] == 1
    assert [item["id"] for item in body["data"]["items"]] == [content_match.id]

    response = client.get("/api/v1/posts?page=1&size=10&keyword=数学")

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["total"] == 1
    assert [item["id"] for item in body["data"]["items"]] == [title_match.id]


def test_list_posts_hot_sort_uses_activity_counts(
    client: TestClient, session: Session
):
    author = create_user(session, "hotpostauthor")
    liker_one = create_user(session, "hotlikerone")
    liker_two = create_user(session, "hotlikertwo")

    viewed_post = create_post(session, author, title="Viewed Post", view_count=20)
    discussed_post = create_post(session, author, title="Discussed Post", view_count=5)
    liked_post = create_post(session, author, title="Liked Post", view_count=5)

    create_comment(session, author, discussed_post, "First discussion")
    create_comment(session, author, discussed_post, "Second discussion")
    create_like(session, liker_one, liked_post)
    create_like(session, liker_two, liked_post)

    response = client.get("/api/v1/posts?page=1&size=10&sort=hot")

    assert response.status_code == 200
    titles = [item["title"] for item in response.json()["data"]["items"]]
    assert titles[:3] == ["Viewed Post", "Discussed Post", "Liked Post"]


def test_read_post_success(client: TestClient, session: Session):
    user = create_user(session, "readpost")
    post = create_post(session, user, title="Readable Post")
    create_comment(session, user, post, "Detail comment")
    create_like(session, user, post)

    response = client.get(f"/api/v1/posts/{post.id}")

    assert response.status_code == 200
    body = response.json()
    assert body["code"] == 200
    assert body["data"]["id"] == post.id
    assert body["data"]["title"] == "Readable Post"
    assert body["data"]["view_count"] == 1
    assert body["data"]["comment_count"] == 1
    assert body["data"]["like_count"] == 1
    assert body["data"]["liked_by_current_user"] is False

    session.refresh(post)
    assert post.view_count == 1


def test_read_post_marks_current_user_like(client: TestClient, session: Session):
    author = create_user(session, "likeddetailauthor")
    liker = create_user(session, "likeddetailuser")
    post = create_post(session, author, title="Liked Detail Post")
    create_like(session, liker, post)

    response = client.get(
        f"/api/v1/posts/{post.id}",
        headers=auth_headers(liker),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["liked_by_current_user"] is True
    assert body["data"]["like_count"] == 1


def test_read_registered_only_post_requires_login(
    client: TestClient, session: Session
):
    user = create_user(session, "privatepostauthor")
    post = create_post(session, user, title="Private Detail", registered_only=True)

    guest_response = client.get(f"/api/v1/posts/{post.id}")
    assert guest_response.status_code == 401
    assert guest_response.json()["message"] == "login required to view this post"

    auth_response = client.get(
        f"/api/v1/posts/{post.id}",
        headers=auth_headers(user),
    )
    assert auth_response.status_code == 200
    assert auth_response.json()["data"]["registered_only"] is True


def test_report_post_success_and_duplicate_pending_blocked(
    client: TestClient, session: Session
):
    author = create_user(session, "reportpostauthor")
    reporter = create_user(session, "reporter")
    post = create_post(session, author, title="Reportable Post")

    response = client.post(
        f"/api/v1/posts/{post.id}/reports",
        json={"reason": "广告营销", "description": "重复广告"},
        headers=auth_headers(reporter),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["post_id"] == post.id
    assert body["data"]["reporter_id"] == reporter.id
    assert body["data"]["reason"] == "广告营销"
    assert body["data"]["status"] == "pending"

    duplicate_response = client.post(
        f"/api/v1/posts/{post.id}/reports",
        json={"reason": "广告营销", "description": "重复广告"},
        headers=auth_headers(reporter),
    )

    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["message"] == "report already submitted"


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
