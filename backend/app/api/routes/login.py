from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core.config import settings
from app.core.security import create_access_token
from app.models import Message, Token, UserCreate, UserPublic, UserUpdate

router = APIRouter(tags=["auth"])


@router.post("/access-token", summary="Login: get JWT access token")
def login_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return Token(
        access_token=create_access_token(
            user.id, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    )


@router.get("/me", response_model=UserPublic, summary="Get current authenticated user")
def get_me(current_user: CurrentUser) -> Any:
    return current_user


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=201,
    dependencies=[Depends(get_current_active_superuser)],
    summary="Register a new user (superuser only)",
)
def register_user(session: SessionDep, body: UserCreate) -> Any:
    existing = crud.get_user_by_email(session=session, email=body.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(session=session, user_in=body)


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