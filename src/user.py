from logging import getLogger
from typing import Union
from uuid import UUID
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from .models.user import ShowUser
from .models.user import UserCreate
from src.serializer.dals_user import UserDAL, LoginDAL
from src.database.config import get_db
from .schemas.authentication import LoginModel

logger = getLogger(__name__)

user_route = APIRouter()


async def login_user(body: LoginModel, db, Authorize: AuthJWT = Depends()):
    async with db as session:
        async with session.begin():
            login_dal = LoginDAL(session)
            login = await login_dal.login_user(LoginModel)
            return login


async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                nickname=body.nickname,
                email_address=body.email_address,
                password=body.password
            )
            return ShowUser(
                user_id=user.user_id,
                nickname=user.nickname,
                email_address=user.email_address,
                is_active=user.is_active,
            )


async def _delete_user(user_id, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            deleted_user_id = await user_dal.delete_user(
                user_id=user_id,
            )
            return deleted_user_id


async def _update_user(
        updated_user_params: dict, user_id: UUID, db
) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            updated_user_id = await user_dal.update_user(
                user_id=user_id, **updated_user_params
            )
            return updated_user_id


async def _get_user_by_id(user_id, db) -> Union[ShowUser, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(
                user_id=user_id,
            )
            if user is not None:
                return ShowUser(
                    user_id=user.user_id,
                    nickname=user.nickname,
                    email_address=user.email_address,
                    is_active=user.is_active,
                )
