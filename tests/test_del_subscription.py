from uuid import UUID

from fastapi import Depends, HTTPException, APIRouter
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import get_db
from src.modules.subscription import set_subscription_user, delete_subscription_user
from src.schemas.user import UpdatePremiumStatus

testx_router = APIRouter(tags=['testx'])


@testx_router.post('/test_after_delete')
async def test_handle(user_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        updated_user_id = await set_subscription_user(user_id=user_id, db=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatePremiumStatus(is_subscriber=updated_user_id)


@testx_router.delete('/delete')
async def del_test_handle(user_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        updated_user_id = await delete_subscription_user(user_id=user_id, db=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatePremiumStatus(is_subscriber=updated_user_id)
