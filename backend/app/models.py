from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False


class UserUpdate(BaseModel):
    is_active: bool | None = None
    is_superuser: bool | None = None


class UserPublic(UserBase):
    id: int


class Message(BaseModel):
    message: str
