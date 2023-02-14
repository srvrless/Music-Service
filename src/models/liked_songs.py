import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.database.config import Base


class LikedSong(Base):
    __tablename__ = "liked_song"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer,primary_key=True)
    song_id = Column(UUID, ForeignKey('song.song_id'))
    user_id = Column(UUID, ForeignKey('user.user_id'))
    title = Column(String, ForeignKey('song.title'))
    creator = Column(String, ForeignKey('song.creator'))
    song_file = Column(String, ForeignKey('song.song_file'))
    verified = Column(Boolean, ForeignKey('song.verified'))
    is_liked = Column(Boolean(), default=False)
