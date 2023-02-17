from logging import getLogger
from typing import Union
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src import settings
from src.database.config import get_db
from src.models.user import User
from src.schemas.authentication import ShowSignUp
from src.schemas.authentication import SignUpModel
from src.layouts.dal_user import UserDAL
from src.utils.hashing import Hasher

logger = getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def create_new_user(user: SignUpModel, db) -> ShowSignUp:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                nickname=user.nickname,
                email_address=user.email_address,
                hashed_password=Hasher.get_password_hash(user.password),
            )
            return ShowSignUp(
                user_id=user.user_id,
                nickname=user.nickname,
                email_address=user.email_address,
                is_active=user.is_active,
            )


async def update_user(
        updated_user_params: dict, user_id: UUID, db) -> Union[UUID, None]:
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


async def delete_user(user_id, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            deleted_user_id = await user_dal.delete_user_data(
                user_id=user_id,
            )
            return deleted_user_id


async def get_user_by_email_for_auth(nickname: str, db: AsyncSession):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            return await user_dal.get_user_by_email(
                nickname=nickname,
            )


async def authenticate_user(nickname: str, password: str, db: AsyncSession
                            ) -> Union[User, None]:
    user = await get_user_by_email_for_auth(nickname=nickname, db=db)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


async def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        nickname: str = payload.get("sub")
        if nickname is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = await get_user_by_email_for_auth(nickname=nickname, db=db)
    if user is None:
        raise credentials_exception
    return user
