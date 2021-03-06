from app.modules.utils.schemas.image import ImageInDB
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDB(UserBase):
    id: Optional[int] = None
    profile_pic: Optional[ImageInDB]

    class Config:
        orm_mode = True


class User(UserInDB):
    pass
