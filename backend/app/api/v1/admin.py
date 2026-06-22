from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.api.deps import AdminUserDep, SessionDep
from app.core.response import error, success
from app.schemas.sensitive_word import (
    SensitiveWordCreate,
    SensitiveWordListRead,
    SensitiveWordRead,
)
from app.services.sensitive_word_service import (
    create_word,
    delete_word,
    get_word_by_id,
    list_words,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/sensitive-words")
def read_sensitive_words(
    session: SessionDep,
    _admin: AdminUserDep,
    keyword: str | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 100,
):
    items, total = list_words(session, keyword=keyword, limit=limit)
    payload = SensitiveWordListRead(
        items=[SensitiveWordRead.model_validate(item) for item in items],
        total=total,
    )
    return success(payload.model_dump(mode="json"))


@router.post("/sensitive-words")
def create_sensitive_word(
    payload: SensitiveWordCreate,
    session: SessionDep,
    _admin: AdminUserDep,
):
    word = create_word(session, payload)
    return success(SensitiveWordRead.model_validate(word).model_dump(mode="json"))


@router.delete("/sensitive-words/{word_id}")
def delete_sensitive_word(
    word_id: int,
    session: SessionDep,
    _admin: AdminUserDep,
):
    word = get_word_by_id(session, word_id)
    if word is None:
        return JSONResponse(
            status_code=404,
            content=error(message="sensitive word not found", code=404),
        )

    delete_word(session, word)
    return success({"deleted": True, "word_id": word_id})
