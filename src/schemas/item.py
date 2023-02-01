
from typing import Optional

from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True



class ItemModel(BaseModel):
    id: Optional[int]
    name: str
    description: str
    price: int
    on_offer: Optional[bool]


class ShowItem(TunedModel):
    id: Optional[int]
    name: str
    description: str
    price: int
    on_offer: Optional[bool]

