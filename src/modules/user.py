from logging import getLogger
from typing import Union
from uuid import UUID
from fastapi import APIRouter

from src.schemas.authentication import ShowSignUp, LoginModel, ShowLogin
from src.schemas.authentication import SignUpModel
from src.serializer.dal_user import UserDAL

logger = getLogger(__name__)


async def logged_in_user(user: LoginModel, db) -> ShowLogin:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.login_user(
                nickname=user.nickname)

async def create_new_user(user: SignUpModel, db) -> ShowSignUp:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                nickname=user.nickname,
                email_address=user.email_address,
                password=user.password
            )
            return ShowSignUp(
                user_id=user.user_id,
                nickname=user.nickname,
                email_address=user.email_address,
                is_active=user.is_active,
            )


async def delete_user(user_id, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            deleted_user_id = await user_dal.delete_user(
                user_id=user_id,
            )
            return deleted_user_id


async def update_user(
    updated_user_params: dict, user_id: UUID, db
) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            updated_user_id = await user_dal.update_user(
                user_id=user_id, **updated_user_params
            )
            return updated_user_id


async def get_user_by_id(user_id, db) -> Union[ShowSignUp, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(
                user_id=user_id,
            )
            if user is not None:
                return ShowSignUp(
                    user_id=user.user_id,
                    nickname=user.nickname,
                    email_address=user.email_address,
                    is_active=user.is_active,
                )

