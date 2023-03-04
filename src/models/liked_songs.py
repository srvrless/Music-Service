from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.database.config import Base


class LikedSong(Base):
    __tablename__ = "liked_song"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    song_id = Column(UUID, ForeignKey('song.song_id'))
    user_id = Column(UUID, ForeignKey('user.user_id'))
