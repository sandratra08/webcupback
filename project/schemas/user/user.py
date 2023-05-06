from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, Field

from tortoise import fields, timezone

from project.utils.password import generate_token


class BaseUser(BaseModel):

    name: str
    first_name: str
    gender: str
    birth_date: datetime
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserDB(BaseUser):
    id: int


def get_expiration_date(duration_seconds: int = 86400) -> datetime:
    return timezone.now() + timedelta(seconds=duration_seconds)


class AccessTokenBase(BaseModel):
    user_id: int
    access_token: str = Field(default_factory=generate_token)
    expiration_date: datetime = Field(default_factory=get_expiration_date)

    class Config:
        orm_mode = True
