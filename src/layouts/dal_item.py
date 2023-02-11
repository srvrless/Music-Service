from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item


class ItemDal:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_item(self, name: str, description: str, price: int, on_offer: bool) -> Item:
        new_item = Item(
            name=name,
            description=description,
            price=price,
            on_offer=on_offer
        )
        self.db_session.add(new_item)
        await self.db_session.flush()
        # await self.db_session.commit()

        return new_item
