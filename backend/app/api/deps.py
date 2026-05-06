from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlmodel import Session

from app.core.config import settings
from app.crud import get_or_create_user_by_email
from infrastructure.persistence.database import get_session
from infrastructure.persistence.models import UserTable

SessionDep = Annotated[Session, Depends(get_session)]

_bearer_scheme = HTTPBearer()


def get_current_user(
    session: SessionDep,
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> UserTable:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        id_info = id_token.verify_oauth2_token(
            credentials.credentials,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
        email: str | None = id_info.get("email")
        if not email:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    return get_or_create_user_by_email(session=session, email=email)


CurrentUser = Annotated[UserTable, Depends(get_current_user)]


def get_current_active_user(
    current_user: CurrentUser,
) -> UserTable:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


CurrentActiveUser = Annotated[UserTable, Depends(get_current_active_user)]


def get_current_active_superuser(
    current_user: CurrentActiveUser,
) -> UserTable:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user


