import secrets
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models.email_verification import EmailVerificationCode


class EmailCodeCooldownError(Exception):
    pass


class EmailCodeInvalidError(Exception):
    pass


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def ensure_aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc)


def generate_email_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def create_email_verification_code(
    session: Session,
    email: str,
    code: str | None = None,
) -> str:
    normalized_email = email.lower()
    now = utc_now()
    cooldown_start = now - timedelta(seconds=settings.email_code_resend_seconds)

    recent_statement = (
        select(EmailVerificationCode)
        .where(EmailVerificationCode.email == normalized_email)
        .where(EmailVerificationCode.created_at >= cooldown_start)
        .order_by(EmailVerificationCode.created_at.desc())
    )
    recent = session.exec(recent_statement).first()
    if recent is not None:
        raise EmailCodeCooldownError

    code_value = code or generate_email_code()
    verification = EmailVerificationCode(
        email=normalized_email,
        code_hash=get_password_hash(code_value),
        expires_at=now + timedelta(minutes=settings.email_code_expire_minutes),
    )
    session.add(verification)
    session.commit()
    return code_value


def verify_email_code(session: Session, email: str, code: str) -> None:
    normalized_email = email.lower()
    statement = (
        select(EmailVerificationCode)
        .where(EmailVerificationCode.email == normalized_email)
        .where(EmailVerificationCode.used_at.is_(None))
        .order_by(EmailVerificationCode.created_at.desc())
    )
    verification = session.exec(statement).first()

    if verification is None:
        raise EmailCodeInvalidError

    now = utc_now()
    if ensure_aware_utc(verification.expires_at) < now:
        raise EmailCodeInvalidError

    if verification.attempts >= 5:
        raise EmailCodeInvalidError

    verification.attempts += 1
    if not verify_password(code, verification.code_hash):
        session.add(verification)
        session.commit()
        raise EmailCodeInvalidError

    verification.used_at = now
    session.add(verification)
    session.commit()


def delete_latest_unused_email_code(session: Session, email: str) -> None:
    normalized_email = email.lower()
    statement = (
        select(EmailVerificationCode)
        .where(EmailVerificationCode.email == normalized_email)
        .where(EmailVerificationCode.used_at.is_(None))
        .order_by(EmailVerificationCode.created_at.desc())
    )
    verification = session.exec(statement).first()
    if verification is None:
        return

    session.delete(verification)
    session.commit()
