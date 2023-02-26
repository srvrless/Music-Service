from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import get_db
from src.models.user import User
from src.modules.user import create_new_user, update_user, get_user_by_id, get_current_user_from_token, \
    authenticate_user, delete_user
from src.schemas.user import ShowSignUp, DeleteUserResponse, SignUpModel, UpdatedUserResponse, \
    UpdateUserRequest, Token
from src.utils.jwt_token import create_access_token

user_router = APIRouter(tags=['user'])


@user_router.post("/login", response_model=Token)
async def jwt_login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect nickname or password",
        )
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user.email_address, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/jwt_auth")
async def sample_endpoint_under_jwt(
        current_user: User = Depends(get_current_user_from_token),
):
    return {"Success": True, "current_user": current_user}


@user_router.post("/", response_model=ShowSignUp)
async def create_user(body: SignUpModel, db: AsyncSession = Depends(get_db)) -> ShowSignUp:
    try:
        logger.info("creating user")
        return await create_new_user(body, db)

    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user_page(
        user_id: UUID, db: AsyncSession = Depends(get_db)
) -> DeleteUserResponse:
    deleted_user_id = await delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.get("/", response_model=ShowSignUp)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowSignUp:
    user = await get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(user_id: UUID, body: UpdateUserRequest, db: AsyncSession = Depends(get_db)
                            ) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user = await get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    try:
        updated_user_id = await update_user(
            updated_user_params=updated_user_params, user_id=user_id, db=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)

    # return {"Success": True, "current_user": db.user_id}

# @user_router.post('/update_profile_image', response_model=create_upload_file)
# async def update_photo():
#     pass
