from typing import Union
from uuid import UUID

from sqlalchemy import and_, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, nickname: str, email_address: str, hashed_password: str) -> User:
        # user = select(User).where(User.email_address == email_address)
        new_user = User(
            nickname=nickname,
            email_address=email_address,
            hashed_password=hashed_password
        )
        # if not user:
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user_data(self, user_id: UUID):
        query = (
            delete(User)
            .where(User.user_id == user_id)
        )
        await self.db_session.execute(query)

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

    async def get_user_by_email(self, nickname: str) -> Union[User, None]:
        query = select(User).where(User.nickname == nickname)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]