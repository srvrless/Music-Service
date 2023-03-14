from sqlalchemy_utils import ChoiceType
from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import ChoiceType

from src.database.config import Base



class PlayList(Base):

    __tablename__ = 'PlayList'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    # order_status = Column(ChoiceType(choices=SONG_STATUS_PLAYLIST), default="NOT_IN_PLAYLIST")
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.user_id'))
    song_id = Column(UUID(as_uuid=True), ForeignKey('song.song_id'))

    def __repr__(self):
        return f"<Order {self.id}>"