from fastapi import APIRouter, status, Depends, HTTPException
from psycopg2 import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import get_db
from src.modules.item import get_all_items
from src.modules.user import logger
from src.schemas.item import ShowItem, ItemModel

item_router = APIRouter(prefix='/item', tags=['item'])


@item_router.post('/items', response_model=ShowItem, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemModel, db: AsyncSession = Depends(get_db)) -> ShowItem:
    try:
        return await get_all_items(item, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
# @app.get('/item/{item_id}', response_model=ItemModel, status_code=status.HTTP_200_OK)
# def get_an_item(item_id: int):
# async with db as session:
#     async with session.begin():
#         item = session.query(Item).filter(Item.id == item_id).first()
#         return item
