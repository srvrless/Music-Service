import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.util.preloaded import orm
from sqlalchemy_utils.types import ChoiceType

from src.database.config import Base
from src.models.playlist import PlayList

PlayList = PlayList()


class Song(Base):
    SONG_STATUS = (
        ('LIKED', 'liked'),
        ('NOT_LIKED', 'not_liked')
        # ('IN_PLAYLIST', 'in_playlist'),
        # ('NOT_IN_PLAYLIST', 'not_in_playlist')
    )
    __tablename__ = "song"
    __table_args__ = {'extend_existing': True}
    song_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    creator = Column(String, nullable=False, unique=True)
    song_file = Column(String, nullable=False, unique=True)
    song_status = Column(ChoiceType(choices=SONG_STATUS), default="NOT_LIKED")
    verified = Column(Boolean, unique=False, default=False)
    duration = Column(Integer, CheckConstraint('duration > 60 AND age < 300'), unique=False, default=False)
    date_added = Column(DateTime, default=datetime.utcnow)
    # is_liked = Column(Boolean(), default=False)
    playlist = relationship('PlayList', backref='songs')
    liked_songs = relationship('liked_songs', backref='songs')

    @orm.validates('duration')
    def validate_age(self, key, duration):
        if not 0 < duration < 100:
            raise ValueError(f'Invalid duration {duration}')
        return duration
