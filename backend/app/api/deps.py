from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlmodel import select

from app.models import UserTable
from infrastructure.persistence.database import SessionDep


def get_current_user_id(
    session: SessionDep,
    x_user_email: Annotated[str, Header(alias="X-User-Email")] = "",
) -> int:
    """
    Resolves the authenticated user's ID from the X-User-Email header.

    The frontend is responsible for authentication; this dependency trusts
    the email passed by the frontend (internal network only).
    """
    if not x_user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cabecera X-User-Email requerida.",
        )
    user = session.exec(
        select(UserTable).where(UserTable.email == x_user_email)
    ).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Usuario '{x_user_email}' no encontrado.",
        )
    return user.id


CurrentUserIdDep = Annotated[int, Depends(get_current_user_id)]
