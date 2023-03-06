import uuid
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, constr, EmailStr, validator


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class Google_Token(BaseModel):
    id: int
    token: str

class ShowSignUp(TunedModel):
    user_id: Optional[int]
    nickname: str
    email_address: EmailStr
    is_active: Optional[bool]

class SignUpModel(BaseModel):
    nickname: str
    email_address: EmailStr
    password: str

    @validator("nickname")
    def validate_nickname(cls, value):
        if not value.isalnum():
            raise HTTPException(
                status_code=422, detail="nickname should contains only letters"
            )
        return value

    @validator('password')
    def password_validation(cls, password):
        if not any(char.isupper() for char in password):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in password):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in password):
            raise ValueError('Password must contain at least one digit')
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return password


class CreateUserModel(SignUpModel):
    token: str


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


class UpdatePremiumStatus(BaseModel):
    is_subscriber: Optional[bool]
