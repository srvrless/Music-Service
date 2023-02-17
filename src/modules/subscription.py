from uuid import UUID
from src.layouts.dal_user import UserDAL


async def subscription_user(user_id: UUID, db):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            set_user_status = await user_dal.set_premium_status(
                user_id=user_id)
            return set_user_status


