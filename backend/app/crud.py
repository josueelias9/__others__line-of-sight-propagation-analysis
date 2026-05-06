from sqlmodel import Session, select

from app.models import UserUpdate
from infrastructure.persistence.models import UserTable


def get_user(session: Session, user_id: int) -> UserTable | None:
    return session.get(UserTable, user_id)


def get_user_by_email(session: Session, email: str) -> UserTable | None:
    return session.exec(select(UserTable).where(UserTable.email == email)).first()


def get_or_create_user_by_email(session: Session, email: str) -> UserTable:
    user = get_user_by_email(session=session, email=email)
    if not user:
        user = UserTable(email=email, is_active=True, is_superuser=False)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def update_user(session: Session, db_user: UserTable, user_in: UserUpdate) -> UserTable:
    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
