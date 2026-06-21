from typing import Literal

from sqlalchemy import desc, distinct
from sqlmodel import Session, func, select

from app.models.comment import Comment
from app.models.like import Like
from app.models.post import Post
from app.models.post import utc_now
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate


def _post_with_counts(
    post: Post,
    comment_count: int,
    like_count: int,
    liked_by_current_user: bool = False,
) -> Post:
    object.__setattr__(post, "comment_count", int(comment_count))
    object.__setattr__(post, "like_count", int(like_count))
    object.__setattr__(post, "liked_by_current_user", liked_by_current_user)
    object.__setattr__(post, "author_nickname", post.author.nickname or post.author.username)
    return post


def create_post(session: Session, post_create: PostCreate, author_id: int) -> Post:
    post = Post(
        title=post_create.title,
        content=post_create.content,
        category=post_create.category,
        allow_comments=post_create.allow_comments,
        author_id=author_id,
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return _post_with_counts(post, 0, 0)


def get_posts_paginated(
    session: Session,
    page: int,
    size: int,
    sort: Literal["latest", "hot", "views", "comments", "likes"] = "latest",
    category: str | None = None,
    current_user_id: int | None = None,
) -> tuple[list[Post], int]:
    filters = []
    if category:
        filters.append(Post.category == category)

    total_statement = select(func.count()).select_from(Post).where(*filters)
    total = session.exec(total_statement).one()

    offset = (page - 1) * size
    comment_count = func.count(distinct(Comment.id))
    like_count = func.count(distinct(Like.id))
    hot_score = Post.view_count + comment_count * 3 + like_count * 2
    order_by = {
        "latest": (Post.created_at.desc(),),
        "hot": (desc(hot_score), Post.created_at.desc()),
        "views": (Post.view_count.desc(), Post.created_at.desc()),
        "comments": (desc(comment_count), Post.created_at.desc()),
        "likes": (desc(like_count), Post.created_at.desc()),
    }[sort]

    statement = (
        select(
            Post,
            comment_count,
            like_count,
        )
        .outerjoin(Comment, Comment.post_id == Post.id)
        .outerjoin(Like, Like.post_id == Post.id)
        .join(User, User.id == Post.author_id)
        .where(*filters)
        .group_by(Post.id, User.id)
        .order_by(*order_by)
        .offset(offset)
        .limit(size)
    )
    items = [
        _post_with_counts(
            post,
            comment_count,
            like_count,
            _is_liked_by_user(session, post.id, current_user_id),
        )
        for post, comment_count, like_count in session.exec(statement).all()
    ]
    return items, total


def _is_liked_by_user(
    session: Session,
    post_id: int | None,
    user_id: int | None,
) -> bool:
    if post_id is None or user_id is None:
        return False

    statement = select(Like.id).where(Like.user_id == user_id, Like.post_id == post_id)
    return session.exec(statement).first() is not None


def get_post_by_id(
    session: Session,
    post_id: int,
    current_user_id: int | None = None,
) -> Post | None:
    statement = (
        select(
            Post,
            func.count(distinct(Comment.id)),
            func.count(distinct(Like.id)),
        )
        .outerjoin(Comment, Comment.post_id == Post.id)
        .outerjoin(Like, Like.post_id == Post.id)
        .join(User, User.id == Post.author_id)
        .where(Post.id == post_id)
        .group_by(Post.id, User.id)
    )
    result = session.exec(statement).first()
    if result is None:
        return None

    post, comment_count, like_count = result
    return _post_with_counts(
        post,
        comment_count,
        like_count,
        _is_liked_by_user(session, post.id, current_user_id),
    )


def increment_post_view_count(
    session: Session,
    post_id: int,
    current_user_id: int | None = None,
) -> Post | None:
    post = session.get(Post, post_id)
    if post is None:
        return None

    post.view_count += 1
    session.add(post)
    session.commit()
    return get_post_by_id(session, post_id, current_user_id=current_user_id)


def delete_post(session: Session, post: Post) -> None:
    session.delete(post)
    session.commit()


def update_post(session: Session, post: Post, post_update: PostUpdate) -> Post:
    update_data = post_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)

    post.updated_at = utc_now()
    session.add(post)
    session.commit()
    session.refresh(post)
    return get_post_by_id(session, post.id) or post
