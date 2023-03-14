
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
