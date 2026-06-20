from sqlmodel import Session, func, select

from app.models.comment import Comment
from app.models.post import Post
from app.models.post import utc_now
from app.schemas.post import PostCreate, PostUpdate


def _post_with_comment_count(post: Post, comment_count: int) -> Post:
    object.__setattr__(post, "comment_count", int(comment_count))
    return post


def create_post(session: Session, post_create: PostCreate, author_id: int) -> Post:
    post = Post(
        title=post_create.title,
        content=post_create.content,
        author_id=author_id,
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return _post_with_comment_count(post, 0)


def get_posts_paginated(
    session: Session,
    page: int,
    size: int,
) -> tuple[list[Post], int]:
    total_statement = select(func.count()).select_from(Post)
    total = session.exec(total_statement).one()

    offset = (page - 1) * size
    statement = (
        select(Post, func.count(Comment.id))
        .outerjoin(Comment, Comment.post_id == Post.id)
        .group_by(Post.id)
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(size)
    )
    items = [
        _post_with_comment_count(post, comment_count)
        for post, comment_count in session.exec(statement).all()
    ]
    return items, total


def get_post_by_id(session: Session, post_id: int) -> Post | None:
    statement = (
        select(Post, func.count(Comment.id))
        .outerjoin(Comment, Comment.post_id == Post.id)
        .where(Post.id == post_id)
        .group_by(Post.id)
    )
    result = session.exec(statement).first()
    if result is None:
        return None

    post, comment_count = result
    return _post_with_comment_count(post, comment_count)


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
