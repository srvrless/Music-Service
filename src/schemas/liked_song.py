from typing import Optional

from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True


class ShowLikedSong(TunedModel):
    id: int
    title: str
    creator: str
    verified: Optional[bool]
    is_liked: bool


class LikedSong(BaseModel):
    is_liked: Optional[bool]
