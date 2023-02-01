import uuid

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname = Column(String, nullable=False, unique=True)
    email_address = Column(String, nullable=False, unique=True)
    password = Column(Text, nullable=True)
    is_active = Column(Boolean(), default=True)
    is_subscriber = Column(Boolean(), default=False)

    def __repr__(self):
        return f'<User {self.nickname}'
