from fastapi import APIRouter, Depends, Form, HTTPException, status
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from project.middlewares.user import find_user_by_email, get_current_user, get_user

from project.models import AccessToken, User as TableData
from project.schemas.message import Status
from project.schemas.user.user import BaseUser as BaseData, UserDB
from project.utils.auth import create_access_token

from project.utils.password import get_password_hash
from fastapi.security.oauth2 import OAuth2PasswordBearer


router = APIRouter()
Tortoise.init_models(["project.models"], "models")
pydantyc_model = pydantic_model_creator(TableData)


@router.get("/", status_code=status.HTTP_200_OK)
async def get():
    return await pydantyc_model.from_queryset(TableData.all())


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create(data: BaseData = Depends(find_user_by_email)):
    result = await TableData.create(**data.dict(exclude={'password'}), password=get_password_hash(data.password))
    if status == 201:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="Enregistrement éffectué",
        )
    return result


@router.post("/token")
async def create_token(user: UserDB = Depends(get_user)):
    token = await create_access_token(user)
    return {"access_token": token.access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserDB)
async def connected_user(user: TableData = Depends(get_current_user)):
    return UserDB.from_orm(user)


@router.post("/logout", response_model=Status, status_code=status.HTTP_200_OK)
async def logout_user(user: TableData = Depends(get_current_user), token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    accessToken = await AccessToken.get(
        access_token=token, user=user.id
    )
    if accessToken is not None:
        await AccessToken.delete(accessToken)
    return Status(message=f"Déconnexion éffectuée")
