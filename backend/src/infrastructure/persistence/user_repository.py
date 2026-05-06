from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from infrastructure.persistence.models import UserCreate, UserTable, UserUpdate


def get_user(session: Session, user_id: int) -> UserTable | None:
    return session.get(UserTable, user_id)


def get_user_by_email(session: Session, email: str) -> UserTable | None:
    return session.exec(select(UserTable).where(UserTable.email == email)).first()


def create_user(session: Session, user_in: UserCreate) -> UserTable:
    user = UserTable(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(session: Session, db_user: UserTable, user_in: UserUpdate) -> UserTable:
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    for key, value in update_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def authenticate(session: Session, email: str, password: str) -> UserTable | None:
    user = get_user_by_email(session=session, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
