import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base
from src.models.liked_songs import LikedSong

# PlayList = PlayList()
LikedSong = LikedSong()


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname = Column(String, nullable=False, unique=True)
    email_address = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)
    is_subscriber = Column(Boolean(), default=False)
    hashed_password = Column(String, nullable=False)
    # playlist = relationship('PlayList', backref='user')
    liked = relationship('LikedSong', backref='user')

    def __repr__(self):
        return f'<User {self.nickname}'
