import uuid

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text

from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy_utils.types import ChoiceType
from typing import Optional
from pydantic import constr, EmailStr, validator, BaseModel
from pydantic import BaseModel

from src.database.config import Base


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True


class ShowSong(TunedModel):
    song_id: uuid.UUID
    name: str
    creator: str
    is_liked: bool


class SongCreate(BaseModel):
    name: str
    creator: str


class Song(Base):
    SONG_STATUS = (
        ('LIKED', 'liked'),
        ('NOT_LIKED', 'not_liked')
        # ('IN_PLAYLIST', 'in_playlist'),
        # ('NOT_IN_PLAYLIST', 'not_in_playlist')
    )
    __tablename__ = "songs"
    __table_args__ = {'extend_existing': True}
    song_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    creator = Column(String, nullable=False, unique=False)
    # song_status = Column(ChoiceType(choices=SONG_STATUS), default="NOT_LIKED")
    song_file = Column(String, nullable=False, unique=True)
    is_liked = Column(Boolean(), default=False)
    # playlist = relationship('PlayList', back_populates='songs')


song = Song


class DeleteSongResponse(BaseModel):
    deleted_song_id: uuid.UUID


class UpdatedSongResponse(BaseModel):
    updated_song_id: uuid.UUID


class UpdateSongRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    creator: Optional[constr(min_length=1)]
