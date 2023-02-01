import uuid

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base

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
    song_file = Column(String, nullable=False, unique=True)
    song_status = Column(ChoiceType(choices=SONG_STATUS), default="NOT_LIKED")
    verified = Column(Boolean, unique=False, default=False)
    # is_liked = Column(Boolean(), default=False)
    # playlist = relationship('PlayList', back_populates='songs')
