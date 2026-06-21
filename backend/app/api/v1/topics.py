from typing import Annotated

from fastapi import APIRouter, Query

from app.api.deps import SessionDep
from app.core.response import success
from app.schemas.topic import TopicListRead, TopicRead
from app.services.topic_service import list_hot_topics, list_topics


router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("")
def read_topics(
    session: SessionDep,
    keyword: str | None = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
):
    topics = list_topics(session, keyword=keyword, limit=limit)
    payload = TopicListRead(items=[TopicRead.model_validate(topic) for topic in topics])
    return success(payload.model_dump(mode="json"))


@router.get("/hot")
def read_hot_topics(
    session: SessionDep,
    limit: Annotated[int, Query(ge=1, le=20)] = 8,
):
    topics = list_hot_topics(session, limit=limit)
    payload = TopicListRead(items=[TopicRead.model_validate(topic) for topic in topics])
    return success(payload.model_dump(mode="json"))
