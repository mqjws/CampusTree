from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import distinct
from sqlmodel import Session, func, select

from app.core.security import get_password_hash, verify_password
from app.models.comment import Comment
from app.models.like import Like
from app.models.post import Post
from app.models.user import User
from app.schemas.user import UserCreate


def _post_with_counts(post: Post, comment_count: int, like_count: int) -> Post:
    object.__setattr__(post, "comment_count", int(comment_count))
    object.__setattr__(post, "like_count", int(like_count))
    object.__setattr__(post, "author_nickname", post.author.nickname or post.author.username)
    object.__setattr__(post, "topic_name", post.topic.name if post.topic else None)
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
        nickname=user_create.username,
        email=str(user_create.email),
        hashed_password=get_password_hash(user_create.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_posts_by_user_id(session: Session, user_id: int) -> list[Post]:
    statement = (
        select(
            Post,
            func.count(distinct(Comment.id)),
            func.count(distinct(Like.id)),
        )
        .outerjoin(Comment, Comment.post_id == Post.id)
        .outerjoin(Like, Like.post_id == Post.id)
        .where(Post.author_id == user_id)
        .group_by(Post.id)
        .order_by(Post.created_at.desc())
    )
    return [
        _post_with_counts(post, comment_count, like_count)
        for post, comment_count, like_count in session.exec(statement).all()
    ]


def get_comments_by_user_id(session: Session, user_id: int) -> list[Comment]:
    statement = (
        select(Comment)
        .where(Comment.author_id == user_id)
        .order_by(Comment.created_at.desc())
    )
    comments = list(session.exec(statement).all())
    for comment in comments:
        object.__setattr__(
            comment,
            "author_nickname",
            comment.author.nickname or comment.author.username,
        )
        object.__setattr__(comment, "post_title", comment.post.title)
    return comments


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
    view_count_statement = (
        select(func.coalesce(func.sum(Post.view_count), 0))
        .select_from(Post)
        .where(Post.author_id == user_id)
    )
    latest_post_at_statement = (
        select(func.max(Post.created_at)).select_from(Post).where(Post.author_id == user_id)
    )
    latest_comment_at_statement = (
        select(func.max(Comment.created_at))
        .select_from(Comment)
        .where(Comment.author_id == user_id)
    )

    post_count = session.exec(post_count_statement).one()
    comment_count = session.exec(comment_count_statement).one()
    like_count = session.exec(like_count_statement).one()
    view_count = session.exec(view_count_statement).one()
    latest_post_at = session.exec(latest_post_at_statement).one()
    latest_comment_at = session.exec(latest_comment_at_statement).one()

    return {
        "post_count": int(post_count),
        "comment_count": int(comment_count),
        "like_count": int(like_count),
        "view_count": int(view_count),
        "latest_post_at": latest_post_at,
        "latest_comment_at": latest_comment_at,
    }


def _count_by_day(
    session: Session,
    model,
    user_field,
    user_id: int,
    start_at: datetime,
) -> dict[date, int]:
    day = func.date(model.created_at)
    statement = (
        select(day, func.count())
        .select_from(model)
        .where(user_field == user_id, model.created_at >= start_at)
        .group_by(day)
    )

    counts: dict[date, int] = {}
    for raw_day, count in session.exec(statement).all():
        if isinstance(raw_day, date):
            parsed_day = raw_day
        else:
            parsed_day = date.fromisoformat(str(raw_day))
        counts[parsed_day] = int(count)
    return counts


def get_user_activity(session: Session, user_id: int, days: int = 90) -> list[dict[str, int | date]]:
    today = datetime.now(timezone.utc).date()
    start_day = today - timedelta(days=days - 1)
    start_at = datetime.combine(start_day, time.min, tzinfo=timezone.utc)

    post_counts = _count_by_day(session, Post, Post.author_id, user_id, start_at)
    comment_counts = _count_by_day(session, Comment, Comment.author_id, user_id, start_at)
    like_counts = _count_by_day(session, Like, Like.user_id, user_id, start_at)

    items = []
    for offset in range(days):
        current_day = start_day + timedelta(days=offset)
        post_count = post_counts.get(current_day, 0)
        comment_count = comment_counts.get(current_day, 0)
        like_count = like_counts.get(current_day, 0)
        score = post_count * 3 + comment_count * 2 + like_count
        items.append(
            {
                "date": current_day,
                "post_count": post_count,
                "comment_count": comment_count,
                "like_count": like_count,
                "score": score,
            }
        )

    return items


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


def update_user_profile(session: Session, user: User, nickname: str) -> User:
    user.nickname = nickname.strip()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
