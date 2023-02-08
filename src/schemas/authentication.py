import re
import uuid
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, constr, EmailStr, validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class ShowLogin(TunedModel):
    username: str
    hashed_password: str


class ShowSignUp(TunedModel):
    user_id: Optional[int]
    nickname: str
    email_address: str
    is_active: Optional[bool]
    is_subscriber: Optional[bool]


class SignUpModel(BaseModel):
    nickname: str
    email_address: str
    password: str

    @validator("nickname")
    def validate_nickname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="nickname should contains only letters"
            )
        return value


class LoginModel(BaseModel):
    nickname: str
    password: str


class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID


class UpdateUserRequest(BaseModel):
    nickname: Optional[constr(min_length=1)]
    email_address: Optional[EmailStr]
