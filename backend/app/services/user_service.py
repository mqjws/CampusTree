from sqlmodel import Session, func, select

from app.core.security import get_password_hash, verify_password
from app.models.comment import Comment
from app.models.like import Like
from app.models.post import Post
from app.models.user import User
from app.schemas.user import UserCreate


def _post_with_comment_count(post: Post, comment_count: int) -> Post:
    object.__setattr__(post, "comment_count", int(comment_count))
    return post


def get_user_by_username(session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def get_user_by_account(session: Session, account: str) -> User | None:
    statement = select(User).where((User.username == account) | (User.email == account))
    return session.exec(statement).first()


def create_user(session: Session, user_create: UserCreate) -> User:
    user = User(
        username=user_create.username,
        email=str(user_create.email),
        hashed_password=get_password_hash(user_create.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_posts_by_user_id(session: Session, user_id: int) -> list[Post]:
    statement = (
        select(Post, func.count(Comment.id))
        .outerjoin(Comment, Comment.post_id == Post.id)
        .where(Post.author_id == user_id)
        .group_by(Post.id)
        .order_by(Post.created_at.desc())
    )
    return [
        _post_with_comment_count(post, comment_count)
        for post, comment_count in session.exec(statement).all()
    ]


def get_comments_by_user_id(session: Session, user_id: int) -> list[Comment]:
    statement = (
        select(Comment)
        .where(Comment.author_id == user_id)
        .order_by(Comment.created_at.desc())
    )
    return list(session.exec(statement).all())


def get_user_stats(session: Session, user_id: int) -> dict[str, int]:
    post_count_statement = select(func.count()).select_from(Post).where(Post.author_id == user_id)
    comment_count_statement = (
        select(func.count()).select_from(Comment).where(Comment.author_id == user_id)
    )
    like_count_statement = (
        select(func.count())
        .select_from(Like)
        .join(Post, Like.post_id == Post.id)
        .where(Post.author_id == user_id)
    )

    post_count = session.exec(post_count_statement).one()
    comment_count = session.exec(comment_count_statement).one()
    like_count = session.exec(like_count_statement).one()

    return {
        "post_count": int(post_count),
        "comment_count": int(comment_count),
        "like_count": int(like_count),
    }


def update_user_password(
    session: Session, user: User, old_password: str, new_password: str
) -> tuple[bool, str]:
    if not verify_password(old_password, user.hashed_password):
        return False, "invalid current password"

    user.hashed_password = get_password_hash(new_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return True, "password updated"
