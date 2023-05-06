from time import timezone
from typing import cast
from project.schemas.message import Status
from project.schemas.user.auth import AuthForm
from project.models import AccessToken, User
from fastapi.security.oauth2 import OAuth2PasswordBearer
from tortoise.exceptions import DoesNotExist
from fastapi import Depends, status, HTTPException
from tortoise import Tortoise, timezone
from project.schemas.user.user import BaseUser

from project.utils.auth import authenticate

Tortoise.init_models(["project.models"], "models")


async def get_connected_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),):
    try:
        access_token: AccessToken = await AccessToken.get(
            access_token=token
        ).prefetch_related("user")
        return cast(User, access_token.user)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification invalide",
            headers={"WWW-Autheticate": "Bearer"}
        )


async def get_current_user(user: User = Depends(get_connected_user)):
    return user


async def get_current_type_user(user: User = Depends(get_connected_user)):
    return user


async def find_user_by_email(user: BaseUser):
    await not_exists_user('email', email=user.email)
    return user


async def not_exists_user(field: str, **kwargs):
    if await User.filter(**kwargs).first() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{field} already exists."
        )


async def get_user(form_data: AuthForm):
    user = await authenticate(form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
