import asyncio
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.payment import check_if_successful_payment
from src.database.config import get_db
from src.modules.subscription import set_subscription_user, delete_subscription_user, delete_expired_subscriptions
from src.modules.user import get_user_by_id
from src.schemas.user import UpdatePremiumStatus

subscribe_router = APIRouter(tags=['subscribe'])


async def schedule_expired_subscriptions_cleanup(db: AsyncSession, background_tasks: BackgroundTasks):
    async def run_cleanup():
        await delete_expired_subscriptions(db)

    # задаем начальную дату выполнения задания
    next_run_time = datetime.now() + timedelta(days=1)

    # создаем периодическое задание
    async def periodic_cleanup():
        nonlocal next_run_time
        while True:
            await asyncio.sleep((next_run_time - datetime.now()).total_seconds())
            background_tasks.add_task(run_cleanup)
            next_run_time += timedelta(days=1)

    # запускаем задание
    asyncio.create_task(periodic_cleanup())


@subscribe_router.post("/set_premium_status")
async def set_premium_subscriber(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(user_id, db)
    if check_if_successful_payment():
        if user is None:
            raise HTTPException(
                status_code=404, detail=f"User with id {user_id} not found."
            )
        try:
            updated_user_id = await set_subscription_user(user_id=user_id, db=db)
        except IntegrityError as err:
            logger.error(err)
            raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatePremiumStatus(is_subscriber=updated_user_id)


@subscribe_router.delete("/delete_subscription")
async def delete_sub(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(user_id, db)
    try:
        updated_user_id = await delete_subscription_user(user_id=user_id, db=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatePremiumStatus(is_subscriber=updated_user_id)
