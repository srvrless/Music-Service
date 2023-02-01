import uuid
from typing import Optional

from pydantic import BaseModel, constr


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True


class SongModel(TunedModel):
    song_id: uuid.UUID
    name: str
    creator: str
    song_file: str
    song_status: Optional[str] = 'NOT_LIKED'
    verified: Optional[bool]


class SongCreate(BaseModel):
    name: str
    creator: str
    song_file: str
    song_status: Optional[str] = 'NOT_LIKED'
    verified: Optional[bool]

class DeleteSongResponse(BaseModel):
    deleted_song_id: uuid.UUID


class UpdatedSongResponse(BaseModel):
    updated_song_id: uuid.UUID


class UpdateSongRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    creator: Optional[constr(min_length=1)]
