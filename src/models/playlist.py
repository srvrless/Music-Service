# from sqlalchemy_utils import ChoiceType
# from sqlalchemy import Integer, Column, ForeignKey
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy_utils import ChoiceType
#
# from src.database.config import Base
#
#
# class PlayList(Base):
#
#     __tablename__ = 'PlayList'
#     id = Column(Integer, primary_key=True)
#     quantity = Column(Integer, nullable=False)
#     # order_status = Column(ChoiceType(choices=SONG_STATUS_PLAYLIST), default="NOT_IN_PLAYLIST")
#     user_id = Column(UUID(as_uuid=True), ForeignKey('user.user_id'))
#     song_id = Column(UUID(as_uuid=True), ForeignKey('song.song_id'))
#
#     def __repr__(self):
#         return f"<Order {self.id}>"
import uuid

from sqlalchemy import Column, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID

from src.database.config import Base


class Subscription(Base):
    __tablename__ = 'subscription'
    __table_args__ = {'extend_existing': True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey('user.user_id'))
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    is_subscriber = Column(Boolean(), default=False)
