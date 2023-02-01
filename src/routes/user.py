from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import get_db
from src.modules.user import create_new_user, update_user, logged_in_user
from src.modules.user import get_user_by_id
from src.schemas.authentication import ShowSignUp, DeleteUserResponse, SignUpModel, UpdatedUserResponse, \
    UpdateUserRequest, ShowLogin, LoginModel

logger = getLogger(__name__)

user_route = APIRouter(prefix='/user', tags=['user'])


#
@user_route.post("/login", response_model=ShowLogin)
async def login_user(body: LoginModel, db: AsyncSession = Depends(get_db)) -> ShowLogin:
    try:
        return await logged_in_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_route.post("/", response_model=ShowSignUp)
async def create_user(body: SignUpModel, db: AsyncSession = Depends(get_db)) -> ShowSignUp:
    try:
        return await create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_route.delete("/", response_model=DeleteUserResponse)
async def delete_user(
        user_id: UUID, db: AsyncSession = Depends(get_db)
) -> DeleteUserResponse:
    deleted_user_id = await delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


# @user_route.get("/", response_model=ShowSignUp)
# async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowSignUp:
#     user = await get_user_by_id(user_id, db)
#     if user is None:
#         raise HTTPException(
#             status_code=404, detail=f"User with id {user_id} not found."
#         )
#     return user


@user_route.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
        user_id: UUID, body: UpdateUserRequest, db: AsyncSession = Depends(get_db)
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
