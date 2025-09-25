from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr


class ProfileBase(BaseModel):
    first_name: Optional[str]
    sur_name: Optional[str]
    last_name: Optional[str]

    email: Optional[EmailStr]
    phone: Optional[str]


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class Profile(ProfileBase):
    pass

    class Config:
        from_attributes=True


class UserBase(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    profile: Optional[ProfileCreate] = None


class UserUpdate(UserBase):
    username: Optional[str]
    password: Optional[str]
    profile: Optional[ProfileUpdate] = None


class ProfileRead(BaseModel):
    first_name: str
    sur_name: str
    last_name: str
    email: str
    phone: str

    class Config:
        from_attributes=True

class UserRead(BaseModel):
    id: uuid.UUID
    username: str
    profile: ProfileRead | None

    class Config:
        from_attributes=True