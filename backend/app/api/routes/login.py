from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.models import Message, UserPublic, UserUpdate

router = APIRouter(tags=["auth"])


@router.get("/me", response_model=UserPublic, summary="Get current authenticated user")
def get_me(current_user: CurrentUser) -> Any:
    return current_user


@router.patch(
    "/users/{user_id}",
    response_model=UserPublic,
    dependencies=[Depends(get_current_active_superuser)],
    summary="Update a user (superuser only)",
)
def update_user(session: SessionDep, user_id: int, body: UserUpdate) -> Any:
    user = crud.get_user(session=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(session=session, db_user=user, user_in=body)


@router.delete(
    "/users/{user_id}",
    response_model=Message,
    dependencies=[Depends(get_current_active_superuser)],
    summary="Delete a user (superuser only)",
)
def delete_user(session: SessionDep, user_id: int) -> Any:
    user = crud.get_user(session=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return Message(message="User deleted successfully")