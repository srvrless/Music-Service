from typing import Union
from uuid import UUID

from pydantic import SecretStr
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.song import Song
from src.models.user import User
from src.schemas.authentication import LoginModel

from fastapi_jwt_auth import AuthJWT

from src.models.user import User
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder

from src.schemas.authentication import LoginModel
class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, nickname: str, email_address: str, password: str) -> User:
        new_user = User(
            nickname=nickname,
            email_address=email_address,
            password=password
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = (
            update(User).where(and_(User.user_id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]


class SongDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_song(self, name: str, creator: str) -> Song:
        new_song = Song(
            name=name,
            creator=creator,
            # duration=duration
        )
        self.db_session.add(new_song)
        await self.db_session.flush()
        return new_song

    async def delete_song(self, song_id: UUID) -> Union[UUID, None]:
        query = (
            update(Song)
            .where(and_(Song.song_id == song_id, Song.is_liked == False))
            .values(is_active=False)
            .returning(Song.song_id)
        )
        res = await self.db_session.execute(query)
        deleted_song_id_row = res.fetchone()
        if deleted_song_id_row is not None:
            return deleted_song_id_row[0]

    async def get_song_by_name(self, song_id: UUID) -> Union[Song, None]:
        query = select(Song)
        res = await self.db_session.execute(query)
        song_row = res.fetchone()
        if song_row is not None:
            return song_row[0]

    async def get_song_by_id(self, song_id: UUID) -> Union[Song, None]:
        query = select(Song).where(Song.song_id == song_id)
        res = await self.db_session.execute(query)
        song_row = res.fetchone()
        if song_row is not None:
            return song_row[0]


class LoginDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def login_user(self, user: LoginModel, password: str, nickname: str) -> User:
        db_user = select(User).where(User.nickname == user.nickname).first()
        if db_user and check_password_hash(db_user.password, user.password):
            access_token = Authorize.create_access_token(subject=db_user.nickname)
            refresh_token = Authorize.create_refresh_token(subject=db_user.nickname)

            response = {
                "access": access_token,
                "refresh": refresh_token
            }

            return jsonable_encoder(response)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid nickname Or Password"
                            )