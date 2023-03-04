import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.util.preloaded import orm

from src.database.config import Base
from src.models.liked_songs import LikedSong

LikedSong = LikedSong()


class Song(Base):
    __tablename__ = "song"
    __table_args__ = {'extend_existing': True}
    song_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    creator = Column(String, nullable=False, unique=True)
    song_file = Column(String)
    img_file = Column(String)
    verified = Column(Boolean, unique=False, default=False)
    date_added = Column(DateTime, default=datetime.utcnow)
    liked_song = relationship('LikedSong', backref='song')

    @orm.validates('duration')
    def validate_age(self, key, duration):
        if not 0 < duration < 100:
            raise ValueError(f'Invalid duration {duration}')
        return duration
