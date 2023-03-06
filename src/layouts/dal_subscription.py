from datetime import datetime, timedelta
from typing import Union
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.subscription import Subscription


class SubscriptionDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def set_premium_status(self, user_id: UUID) -> Union[UUID, None]:
        start_date = datetime.now()
        end_date = start_date + timedelta(days=30)

        set_premium = Subscription(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            is_subscriber=True
        )
        self.db_session.add(set_premium)
        await self.db_session.flush()
        return set_premium

    async def delete_premium_status(self, user_id: UUID) -> Union[UUID, None]:
        query = (
            delete(Subscription)
            .where(Subscription.user_id == user_id)
            .returning(Subscription.is_subscriber)
        )

        result = await self.db_session.execute(query)
        update_user_id_row = result.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def delete_subscription_after_a_while(self) -> Union[UUID, None]:
        now = datetime.now()
        query = (
            delete(Subscription)
            .where(Subscription.end_date < now)
            .returning(Subscription.is_subscriber)
        )

        result = await self.db_session.execute(query)
        update_user_id_row = result.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]
        return update_user_id_row
