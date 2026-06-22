from sqlalchemy import desc
from sqlmodel import Session, func, select

from app.models.post import Post
from app.models.topic import Topic


def normalize_topic_name(name: str | None) -> str | None:
    if name is None:
        return None

    normalized = name.strip().lstrip("#").strip()
    if not normalized:
        return None

    return normalized[:50]


def _topic_with_count(topic: Topic, post_count: int) -> Topic:
    object.__setattr__(topic, "post_count", int(post_count))
    return topic


def get_topic_by_name(session: Session, name: str) -> Topic | None:
    statement = select(Topic).where(Topic.name == name)
    return session.exec(statement).first()


def get_or_create_topic(session: Session, name: str | None) -> Topic | None:
    normalized = normalize_topic_name(name)
    if normalized is None:
        return None

    topic = get_topic_by_name(session, normalized)
    if topic is not None:
        return topic

    topic = Topic(name=normalized)
    session.add(topic)
    session.flush()
    session.refresh(topic)
    return topic


def list_topics(
    session: Session,
    keyword: str | None = None,
    limit: int = 20,
) -> list[Topic]:
    post_count = func.count(Post.id)
    filters = []
    normalized_keyword = normalize_topic_name(keyword)
    if normalized_keyword:
        filters.append(Topic.name.ilike(f"%{normalized_keyword}%"))

    statement = (
        select(Topic, post_count)
        .outerjoin(Post, Post.topic_id == Topic.id)
        .where(*filters)
        .group_by(Topic.id)
        .order_by(desc(post_count), Topic.created_at.desc())
        .limit(limit)
    )
    return [
        _topic_with_count(topic, count)
        for topic, count in session.exec(statement).all()
    ]


def list_hot_topics(session: Session, limit: int = 8) -> list[Topic]:
    post_count = func.count(Post.id)
    statement = (
        select(Topic, post_count)
        .outerjoin(Post, Post.topic_id == Topic.id)
        .group_by(Topic.id)
        .order_by(desc(post_count), Topic.created_at.desc())
        .limit(limit)
    )
    return [
        _topic_with_count(topic, count)
        for topic, count in session.exec(statement).all()
    ]
