from sqlmodel import Session, func, select

from app.models.comment import Comment
from app.models.comment import utc_now
from app.schemas.comment import CommentCreate, CommentUpdate


def _comment_with_author(comment: Comment) -> Comment:
    object.__setattr__(
        comment,
        "author_nickname",
        comment.author.nickname or comment.author.username,
    )
    return comment


def create_comment(
    session: Session, comment_create: CommentCreate, author_id: int, post_id: int
) -> Comment:
    comment = Comment(
        content=comment_create.content,
        author_id=author_id,
        post_id=post_id,
    )
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return _comment_with_author(comment)


def get_comments_by_post_paginated(
    session: Session,
    post_id: int,
    page: int,
    size: int,
) -> tuple[list[Comment], int]:
    total_statement = (
        select(func.count()).select_from(Comment).where(Comment.post_id == post_id)
    )
    total = session.exec(total_statement).one()

    offset = (page - 1) * size
    statement = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.created_at.desc())
        .offset(offset)
        .limit(size)
    )
    items = [_comment_with_author(comment) for comment in session.exec(statement).all()]
    return items, total


def get_comment_by_id(session: Session, comment_id: int) -> Comment | None:
    comment = session.get(Comment, comment_id)
    return _comment_with_author(comment) if comment else None


def update_comment(
    session: Session, comment: Comment, comment_update: CommentUpdate
) -> Comment:
    update_data = comment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(comment, field, value)

    comment.updated_at = utc_now()
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return _comment_with_author(comment)


def delete_comment(session: Session, comment: Comment) -> None:
    session.delete(comment)
    session.commit()
