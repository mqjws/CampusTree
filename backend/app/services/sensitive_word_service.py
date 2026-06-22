from sqlmodel import Session, func, select

from app.models.sensitive_word import SensitiveWord
from app.schemas.sensitive_word import SensitiveWordCreate


def list_words(
    session: Session, keyword: str | None = None, limit: int = 100
) -> tuple[list[SensitiveWord], int]:
    filters = []
    if keyword:
        filters.append(SensitiveWord.word.ilike(f"%{keyword.strip()}%"))

    total_stmt = select(func.count()).select_from(SensitiveWord).where(*filters)
    total = session.exec(total_stmt).one()

    stmt = (
        select(SensitiveWord)
        .where(*filters)
        .order_by(SensitiveWord.created_at.desc())
        .limit(limit)
    )
    items = list(session.exec(stmt).all())
    return items, total


def get_word_by_id(session: Session, word_id: int) -> SensitiveWord | None:
    return session.get(SensitiveWord, word_id)


def create_word(session: Session, payload: SensitiveWordCreate) -> SensitiveWord:
    word = SensitiveWord(word=payload.word.strip())
    session.add(word)
    session.commit()
    session.refresh(word)
    return word


def delete_word(session: Session, word: SensitiveWord) -> None:
    session.delete(word)
    session.commit()


def check_sensitive_words(session: Session, content: str) -> list[str]:
    """检测内容是否包含敏感词，返回命中的敏感词列表"""
    words = list(session.exec(select(SensitiveWord.word)).all())
    matched: list[str] = []
    content_lower = content.lower()
    for word in words:
        if word.lower() in content_lower:
            matched.append(word)
    return matched
