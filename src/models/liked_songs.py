import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils.types import ChoiceType

from src.database.config import Base


class Song(Base):
    SONG_STATUS = (
        ('LIKED', 'liked'),
        ('NOT_LIKED', 'not_liked')
        # ('IN_PLAYLIST', 'in_playlist'),
        # ('NOT_IN_PLAYLIST', 'not_in_playlist')
    )
    __tablename__ = "liked_songs"
    __table_args__ = {'extend_existing': True}
    song_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, ForeignKey('songs.name'))
    creator = Column(String, ForeignKey('songs.creator'))
    song_file = Column(String, ForeignKey('songs.song_file'))
    song_status = Column(ChoiceType(choices=SONG_STATUS), default="NOT_LIKED")
    verified = Column(Boolean, ForeignKey('songs.verified'))
    is_liked = Column(Boolean(), default=False)
