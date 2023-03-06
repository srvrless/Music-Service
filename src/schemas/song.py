import uuid
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, constr


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True


class ShowSong(TunedModel):
    title: str
    creator: str
    song_file: str
    img_file: str


class SongCreate(BaseModel):
    title: str
    creator: str
    img_file: str
    song_file: str


class DeleteSongResponse(BaseModel):
    deleted_song_id: uuid.UUID


class UpdatedSongResponse(BaseModel):
    updated_song_id: uuid.UUID


class UpdateSongRequest(BaseModel):
    title: Optional[constr(min_length=1)]
    creator: Optional[constr(min_length=1)]
    img_file: str
    song_file: str
