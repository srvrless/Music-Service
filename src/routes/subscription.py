import asyncio
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.payment import check_if_successful_payment
from src.database.config import get_db
from src.models.user import User
from src.modules.subscription import set_subscription_user, delete_subscription_user, delete_expired_subscriptions
from src.modules.user import get_user_by_id, get_current_user_from_token
from src.schemas.user import UpdatePremiumStatus

subscribe_router = APIRouter(tags=['subscribe'])


# deleted expired subscription after 30 days
async def schedule_expired_subscriptions_cleanup(db: AsyncSession, background_tasks: BackgroundTasks):
    async def run_cleanup():
        await delete_expired_subscriptions(db)

    # set date do a task
    next_run_time = datetime.now() + timedelta(days=1)

    # create period task
    async def periodic_cleanup():
        nonlocal next_run_time
        while True:
            await asyncio.sleep((next_run_time - datetime.now()).total_seconds())
            background_tasks.add_task(run_cleanup)
            next_run_time += timedelta(days=1)

    # запускаем задание
    asyncio.create_task(periodic_cleanup())


@subscribe_router.post("/set_premium_status")
async def set_premium_subscriber(db: AsyncSession = Depends(get_db),
                                 current_user: User = Depends(get_current_user_from_token)):
    user = await get_user_by_id(current_user.user_id, db)
    if check_if_successful_payment():
        if user is None:
            raise HTTPException(
                status_code=404, detail=f"User with id {current_user.user_id} not found."
            )
        try:
            updated_user_id = await set_subscription_user(user_id=current_user.user_id, db=db)
            return updated_user_id
        except IntegrityError as err:
            logger.error(err)
            raise HTTPException(status_code=503, detail=f"Database error: {err}")


@subscribe_router.delete("/delete_subscription")
async def delete_sub(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(user_id, db)
    try:
        updated_user_id = await delete_subscription_user(user_id=user_id, db=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatePremiumStatus(is_subscriber=updated_user_id)
