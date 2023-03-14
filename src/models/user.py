import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base
from src.models.liked_songs import LikedSong
from src.models.subscription import Subscription
from src.models.song import Song


LikedSong = LikedSong()
Song = Song()
Subscription = Subscription()


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname = Column(String, nullable=False, unique=True)
    email_address = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String, nullable=False)
    user = relationship('Subscription', backref='user')
    user_favorite = relationship('Song', backref='user', secondary='liked_song')

    def __repr__(self):
        return f'<User {self.nickname}'
