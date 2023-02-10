# from typing import Union
#
# import jwt
# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from src.core.settings import Settings
# from src.models.user import User
# from src.modules.authentication import token_generator
# from src.modules.user import oauth2_scheme
# from src.schemas.authentication import LoginModel
# from src.serializer.dal_user import UserDAL
# from src.utils.hashing import Hasher
#
# users = []
# jwt_router = APIRouter(tags=['jwt'])
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, Settings.authjwt_secret_key, algorithms=['HS256'])
#         user = await User.get(id=payload.get("id"))
#     except:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid nickname or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#
#     return user
#
#
# async def get_user_by_email_for_auth(nickname: str, db: AsyncSession):
#     async with db as session:
#         async with session.begin():
#             user_dal = UserDAL(session)
#             return await user_dal.get_user_by_email(nickname=nickname)
#
#
# async def authenticate_user(
#         nickname: str, password: str, db: AsyncSession
# ) -> Union[User, None]:
#     user = await get_user_by_email_for_auth(nickname=nickname, db=db)
#     if user is None:
#         return
#     if Hasher.verify_password(password, user.hashed_password):
#         return user
#
#
# @jwt_router.post('/token')
# async def generate_token(request_from: OAuth2PasswordRequestForm = Depends()):
#     token = await token_generator(request_from.username, request_from.password)
#     return {"access_token": token, "token_type": "bearer"}
#
#
# @jwt_router.post('/user/me')
# async def user_login(user: LoginModel = Depends(get_current_user)):
#     return {"status": "ok",
#             "data":
#                 {
#                     "nickname": user.nickname,
#                     "password": user.password
#
#                 }
#             }
# #
# # @jwt_routerr.get('/jwt_fresh_url')
# # async def get_user(Authorize: AuthJWT = Depends()):
# #     try:
# #         Authorize.fresh_jwt_required()
# #     except Exception as e:
# #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
# #     current_user = Authorize.get_jwt_subject()
# #
# #     return {"current_user": current_user}
