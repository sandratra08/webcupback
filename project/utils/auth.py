from typing import Optional

from project.utils.password import verify_password
from project.models import AccessToken, User
from project.schemas.user.user import AccessTokenBase, UserDB


async def create_access_token(user: UserDB) -> AccessToken:
    access_token = AccessTokenBase(user_id=user.id)
    access_token_tortoise = await AccessToken.create(**access_token.dict())
    return AccessTokenBase.from_orm(access_token_tortoise)


async def authenticate(email: str, password: str) -> Optional[UserDB]:
    user: User = await User.get(email=email)
    if not verify_password(password, user.password):
        return None
    return UserDB.from_orm(user)
