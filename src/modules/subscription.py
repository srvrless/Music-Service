from datetime import datetime
from uuid import UUID

from sqlalchemy import delete

from src.layouts.dal_subscription import SubscriptionDAL
from src.models.subscription import Subscription


async def set_subscription_user(user_id: UUID, db):
    async with db as session:
        async with session.begin():
            sub_dal = SubscriptionDAL(session)
            set_subscription = await sub_dal.set_premium_status(
                user_id=user_id)
            return set_subscription


async def delete_subscription_user(user_id: UUID, db):
    async with db as session:
        async with session.begin():
            sub_dal = SubscriptionDAL(session)
            del_subscribe = await sub_dal.delete_premium_status(
                user_id=user_id)
            return del_subscribe


async def delete_expired_subscriptions(db):
    async with db as session:
        async with session.begin():
            now = datetime.now()
            query = (
                delete(Subscription)
                .where(Subscription.end_date < now)
                .returning(Subscription.is_subscriber)
            )

            result = await session.execute(query)
            update_user_id_row = result.fetchone()
            if update_user_id_row is not None:
                return update_user_id_row[0]
            return update_user_id_row