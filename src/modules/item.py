from fastapi import HTTPException

from src.models.item import Item
from src.schemas.item import ItemModel, ShowItem
from src.serializer.dal_item import ItemDal


async def get_all_items(item: ItemModel, db) -> ShowItem:
    async with db as session:
        async with session.begin():
            item_dal = ItemDal(session)
            items = await item_dal.create_item(
                name=item.name,
                description=item.description,
                price=item.price,
                on_offer=item.on_offer
            )
            #  select yusewr

            if id is None:
                raise HTTPException(status_code=400, detail="Item already exists")

            # db_item = session.select(Item).where(Item.name == item.name).first()

            return ShowItem(
                name=item.name,
                description=item.description,
                price=item.price,
                on_offer=item.on_offer,
            )
