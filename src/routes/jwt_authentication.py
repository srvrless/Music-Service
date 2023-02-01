from typing import Union

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from hashing import Hasher
from src.models.user import User
from src.modules.authentication import token_generator
from src.schemas.authentication import LoginModel
from src.serializer.dal_user import UserDAL

users = []
jwt_router = APIRouter(tags=['jwt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_user_by_email_for_auth(email_address: str, db: AsyncSession):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            return await user_dal.get_user_by_email(email_address=email_address)


async def authenticate_user(
        email_address: str, password: str, db: AsyncSession
) -> Union[User, None]:
    user = await get_user_by_email_for_auth(email_address=email_address, db=db)
    if user is None:
        return
    if Hasher.verify_password(password, user.hashed_password):
        return user


@jwt_router.post('/token')
async def generate_token(request_from: OAuth2PasswordRequestForm = Depends()):
    token = await token_generator(request_from.username, request_from.password)
    return {"access_token": token, "token_type": "bearer"}


@jwt_router.post('/user/me')
async def user_login(user: LoginModel = Depends(get_current_user)):
    return {"status": "ok",
            "data":
                {
                    "username": user.nickname,
                    "password": user.password

                }
            }

# create a new user
# @jwt_router.post('/jwt_signup', status_code=201)
# async def create_user(user: SignUpModel):
#     new_user = {
#         "nickname": user.nickname,
#         "email_address": user.email_address,
#         "password": user.password
#     }
#
#     users.append(new_user)
#
#     return new_user
#
#
# # getting all users
# @jwt_router.get('/jwt_users', response_model=List[SignUpModel])
# async def get_users():
#     return users
#
#
# @jwt_router.post('/jwt_login')
# async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
#     for u in users:
#         if (u["nickname"] == user.nickname) and (u["password"] == user.password):
#             access_token = Authorize.create_access_token(subject=user.nickname)
#             refresh_token = Authorize.create_refresh_token(subject=user.nickname)
#             return {"access_token": access_token, "refresh_token": refresh_token}
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
#
#
# @jwt_router.get('/jwt_protected')
# async def get_logged_in_user(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()
#
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
#     current_user = Authorize.get_jwt_subject()
#
#     return {"current_user": current_user}
#
#
# @jwt_router.get('/jwt_new_token')
# async def create_new_token(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_refresh_token_required()
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
#
#     current_user = Authorize.get_jwt_subject()
#
#     access_token = Authorize.create_access_token(subject=current_user)
#
#     return {"new_access_token": access_token}
#
#
# @jwt_router.post('/jwt_fresh_login')
# async def fresh_login(user: LoginModel, Authorize: AuthJWT = Depends()):
#     for u in users:
#         if (u["nickname"] == user.nickname) and (u["password"] == user.password):
#             fresh_token = Authorize.create_access_token(subject=user.nickname, fresh=True)
#             return {"fresh_token": fresh_token}
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
#
#
# @jwt_router.get('/jwt_fresh_url')
# async def get_user(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.fresh_jwt_required()
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
#     current_user = Authorize.get_jwt_subject()
#
#     return {"current_user": current_user}
