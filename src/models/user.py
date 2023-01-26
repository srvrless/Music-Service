import re
import uuid

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text

from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
from fastapi import HTTPException
from pydantic import constr, EmailStr, validator, BaseModel, SecretStr
from pydantic import BaseModel

from src.database.config import Base

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nickname = Column(String, nullable=False, unique=True)
    email_address = Column(String, nullable=False, unique=True)
    password = Column(Text, nullable=True)
    is_active = Column(Boolean(), default=True)
    is_subscriber = Column(Boolean(), default=True)

    def __repr__(self):
        return f'<User {self.nickname}'





class ShowUser(TunedModel):
    user_id: uuid.UUID
    nickname: str
    email_address: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    nickname: str
    email_address: EmailStr
    password: Optional[str]

    @validator("nickname")
    def validate_nickname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="nickname should contains only letters"
            )
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID


class UpdateUserRequest(BaseModel):
    nickname: Optional[constr(min_length=1)]
    email_address: Optional[EmailStr]

    @validator("nickname")
    def validate_nickname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="nickname should contains only letters"
            )
        return value
