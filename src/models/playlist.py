from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from src.database.config import Base
from sqlalchemy import String, Boolean, Integer, Column, Text, ForeignKey


class PlayList(Base):
    SONG_STATUS_PLAYLIST = (
        ('IN_PLAYLIST', 'in_playlist'),
        ('NOT_IN_PLAYLIST', 'not_in_playlist')
    )
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=SONG_STATUS_PLAYLIST), default="NOT_IN_PLAYLIST")
    user_id = Column(Integer, ForeignKey('user.user_id'))
    songs = relationship('Song', back_populates='playlist')

    def __repr__(self):
        return f"<Order {self.id}>"
