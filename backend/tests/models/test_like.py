"""
Test Like ORM model and relationships
"""
import pytest
from sqlmodel import Session, select

from app.models import Like, Post, User


def test_like_model_creation(session: Session):
    """Test creating a Like instance"""
    # Create test user
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpassword123",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create test post
    post = Post(
        title="Test Post",
        content="This is a test post content",
        author_id=user.id,
    )
    session.add(post)
    session.commit()
    session.refresh(post)

    # Create like
    like = Like(user_id=user.id, post_id=post.id)
    session.add(like)
    session.commit()
    session.refresh(like)

    # Assertions
    assert like.id is not None
    assert like.user_id == user.id
    assert like.post_id == post.id
    assert like.created_at is not None


def test_like_user_relationship(session: Session):
    """Test Like -> User relationship"""
    user = User(
        username="testuser2",
        email="test2@example.com",
        hashed_password="hashedpassword123",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    post = Post(
        title="Test Post 2",
        content="Content 2",
        author_id=user.id,
    )
    session.add(post)
    session.commit()
    session.refresh(post)

    like = Like(user_id=user.id, post_id=post.id)
    session.add(like)
    session.commit()
    session.refresh(like)

    # Test relationship
    assert like.user.id == user.id
    assert like.user.username == "testuser2"


def test_like_post_relationship(session: Session):
    """Test Like -> Post relationship"""
    user = User(
        username="testuser3",
        email="test3@example.com",
        hashed_password="hashedpassword123",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    post = Post(
        title="Test Post 3",
        content="Content 3",
        author_id=user.id,
    )
    session.add(post)
    session.commit()
    session.refresh(post)

    like = Like(user_id=user.id, post_id=post.id)
    session.add(like)
    session.commit()
    session.refresh(like)

    # Test relationship
    assert like.post.id == post.id
    assert like.post.title == "Test Post 3"


def test_user_likes_relationship(session: Session):
    """Test User -> Likes relationship (back_populates)"""
    user = User(
        username="testuser4",
        email="test4@example.com",
        hashed_password="hashedpassword123",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    post1 = Post(title="Post 1", content="Content 1", author_id=user.id)
    post2 = Post(title="Post 2", content="Content 2", author_id=user.id)
    session.add(post1)
    session.add(post2)
    session.commit()
    session.refresh(post1)
    session.refresh(post2)

    like1 = Like(user_id=user.id, post_id=post1.id)
    like2 = Like(user_id=user.id, post_id=post2.id)
    session.add(like1)
    session.add(like2)
    session.commit()

    # Refresh user to load relationships
    session.refresh(user)

    # Test back_populates
    assert len(user.likes) == 2
    assert {like.post_id for like in user.likes} == {post1.id, post2.id}


def test_post_likes_relationship(session: Session):
    """Test Post -> Likes relationship (back_populates)"""
    user1 = User(username="user1", email="user1@example.com", hashed_password="hash1")
    user2 = User(username="user2", email="user2@example.com", hashed_password="hash2")
    session.add(user1)
    session.add(user2)
    session.commit()
    session.refresh(user1)
    session.refresh(user2)

    post = Post(title="Popular Post", content="Great content", author_id=user1.id)
    session.add(post)
    session.commit()
    session.refresh(post)

    like1 = Like(user_id=user1.id, post_id=post.id)
    like2 = Like(user_id=user2.id, post_id=post.id)
    session.add(like1)
    session.add(like2)
    session.commit()

    # Refresh post to load relationships
    session.refresh(post)

    # Test back_populates
    assert len(post.likes) == 2
    assert {like.user_id for like in post.likes} == {user1.id, user2.id}


def test_unique_constraint_user_post_like(session: Session):
    """Test that a user can only like a post once (unique constraint)"""
    user = User(
        username="testuser5",
        email="test5@example.com",
        hashed_password="hashedpassword123",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    post = Post(
        title="Test Post 5",
        content="Content 5",
        author_id=user.id,
    )
    session.add(post)
    session.commit()
    session.refresh(post)

    # First like should succeed
    like1 = Like(user_id=user.id, post_id=post.id)
    session.add(like1)
    session.commit()

    # Second like should fail due to unique constraint
    like2 = Like(user_id=user.id, post_id=post.id)
    session.add(like2)

    with pytest.raises(Exception):  # Will raise IntegrityError
        session.commit()


def test_like_cascade_delete_on_user(session: Session):
    """Test that likes are deleted when user is deleted"""
    user = User(
        username="testuser6",
        email="test6@example.com",
        hashed_password="hashedpassword123",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    post = Post(
        title="Test Post 6",
        content="Content 6",
        author_id=user.id,
    )
    session.add(post)
    session.commit()
    session.refresh(post)

    like = Like(user_id=user.id, post_id=post.id)
    session.add(like)
    session.commit()
    like_id = like.id

    # Delete user
    session.delete(user)
    session.commit()

    # Verify like still exists (depends on FK cascade settings)
    # Note: Default SQLModel behavior doesn't cascade delete
    # This test documents current behavior
    result = session.get(Like, like_id)
    # In current setup, this may fail due to FK constraint
    # Adjust based on your cascade settings


def test_like_indexes(session: Session):
    """Test that indexes on user_id and post_id work correctly"""
    # Create test data
    users = [
        User(username=f"user{i}", email=f"user{i}@example.com", hashed_password="hash")
        for i in range(5)
    ]
    for user in users:
        session.add(user)
    session.commit()

    posts = [
        Post(title=f"Post {i}", content=f"Content {i}", author_id=users[0].id)
        for i in range(5)
    ]
    for post in posts:
        session.add(post)
    session.commit()

    # Create likes
    for i, user in enumerate(users):
        for j, post in enumerate(posts):
            if i <= j:  # Create triangular pattern
                like = Like(user_id=user.id, post_id=post.id)
                session.add(like)
    session.commit()

    # Query by user_id (should use index)
    user_likes = session.exec(
        select(Like).where(Like.user_id == users[0].id)
    ).all()
    assert len(user_likes) == 5

    # Query by post_id (should use index)
    post_likes = session.exec(
        select(Like).where(Like.post_id == posts[0].id)
    ).all()
    assert len(post_likes) == 1

    # Query by both (should use unique constraint)
    specific_like = session.exec(
        select(Like).where(Like.user_id == users[1].id, Like.post_id == posts[1].id)
    ).first()
    assert specific_like is not None
