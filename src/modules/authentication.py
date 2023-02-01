import jwt
from dotenv import dotenv_values
from fastapi import (HTTPException, status, Depends)
from passlib.context import CryptContext

from src.models.user import User

config_credentials = dict(dotenv_values(".env"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(nickname: str, password: str):
    user = await User.query.filter_by(nickname=nickname)

    if user and verify_password(password, user.password):
        return user

    return False


async def token_generator(nickname: str, password: str):
    user = await authenticate_user(nickname, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {
        "user_id": user.user_id,
        "nickname": user.nickname
    }

    token = jwt.encode(token_data, config_credentials["SECRET"])
    return token


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, config_credentials['SECRET'], algorithms=['HS256'])
        user = await User.query.filter_by(user_id=payload.get('user_id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user



