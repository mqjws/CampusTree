from sqlmodel import Session, select

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate


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
        email=str(user_create.email),
        hashed_password=get_password_hash(user_create.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
