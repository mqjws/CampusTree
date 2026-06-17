from sqlmodel import Session, select

from app.models.like import Like


class LikeAlreadyExistsError(Exception):
    pass


class LikeNotFoundError(Exception):
    pass


def get_like_by_user_and_post(
    session: Session,
    user_id: int,
    post_id: int,
) -> Like | None:
    statement = select(Like).where(Like.user_id == user_id, Like.post_id == post_id)
    return session.exec(statement).first()


def like_post(session: Session, user_id: int, post_id: int) -> Like:
    existing_like = get_like_by_user_and_post(
        session,
        user_id=user_id,
        post_id=post_id,
    )
    if existing_like is not None:
        raise LikeAlreadyExistsError

    like = Like(user_id=user_id, post_id=post_id)
    session.add(like)
    session.commit()
    session.refresh(like)
    return like


def unlike_post(session: Session, user_id: int, post_id: int) -> None:
    like = get_like_by_user_and_post(
        session,
        user_id=user_id,
        post_id=post_id,
    )
    if like is None:
        raise LikeNotFoundError

    session.delete(like)
    session.commit()
