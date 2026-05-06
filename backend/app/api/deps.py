from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.core.config import settings
from app.core.security import ALGORITHM
from app.crud import get_user
from app.models import TokenPayload
from infrastructure.persistence.database import get_session
from infrastructure.persistence.models import UserTable

SessionDep = Annotated[Session, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/access-token")

TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(
    session: SessionDep,
    token: TokenDep,
) -> UserTable:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        if token_data.sub is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(session=session, user_id=int(token_data.sub))
    if user is None:
        raise credentials_exception
    return user

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


