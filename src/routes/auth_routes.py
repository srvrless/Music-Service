from fastapi_jwt_auth import AuthJWT

from src.models.user import User
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder

from src.schemas.authentication import LoginModel

auth_router = APIRouter(prefix='/auth', tags=['auth'])


# @auth_router.post('/signup')
# async def signup(user: SignUpModel):
#     # db_email=async_session
#     try:
#         return await _create_new_user(body, db)
#     except IntegrityError as err:
#         logger.error(err)
#         raise HTTPException(status_code=503, detail=f"Database error: {err}")

# @auth_router.post("/auth", response_model=user.TokenBase)
# async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await users_utils.get_user_by_email(email=form_data.username)
#
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect email or password")
#
#     if not users_utils.validate_password(
#         password=form_data.password, hashed_password=user["hashed_password"]
#     ):
#         raise HTTPException(status_code=400, detail="Incorrect email or password")
#
#     return await users_utils.create_user_token(user_id=user["id"])


# @auth_router.post('/signup',
#                   status_code=status.HTTP_201_CREATED
#                   )
# async def signup(user: User, db):
#     async with db as session:
#         async with session.begin():
#             email_address = await session.query(User).filter(User.email_address == user.email_address).first()
#
#             if email_address is not None:
#                 return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                                      detail="User with the email already exists"
#                                      )
#
#             db_username = session.query(User).filter(User.username == user.username).first()
#
#             if db_username is not None:
#                 return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                                      detail="User with the username already exists"
#                                      )
#
#             new_user = User(
#                 username=user.username,
#                 email=user.email,
#                 password=generate_password_hash(user.password),
#                 is_active=user.is_active,
#                 is_staff=user.is_staff
#             )
#
#             session.add(new_user)
#
#             session.commit()
#
#             return new_user


@auth_router.post('/login')
async def login(user: LoginModel, db, Authorize: AuthJWT = Depends()):
    async with db as session:
        async with session.begin():
            db_user = await session.query(User).filter(User.nickname == user.nickname).first()

            if db_user and check_password_hash(db_user.password, user.password):
                access_token = Authorize.create_access_token(subject=db_user.nickname)
                refresh_token = Authorize.create_refresh_token(subject=db_user.nickname)

                response = {
                    "access": access_token,
                    "refresh": refresh_token
                }

                return await jsonable_encoder(response)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Invalid nickname Or Password"
                                )
