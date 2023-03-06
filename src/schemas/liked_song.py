import datetime
from typing import Optional
import uuid

from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True


class LikedSong(TunedModel):
    user_id: uuid.UUID
    song_id: uuid.UUID


class LikedSongModel(BaseModel):
    user_id: uuid.UUID
    song_id: uuid.UUID


class ShowLikedSong(TunedModel):
    id: int
    title: str
    creator: str
    verified: Optional[bool]
    album: Optional[str]
    created_at: datetime.datetime
