from logging import getLogger
from typing import Union
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import DeleteUserResponse
from src.models.user import ShowUser
from src.models.user import UpdatedUserResponse
from src.models.user import UpdateUserRequest
from src.models.user import UserCreate
from src.serializer.dals_user import UserDAL
from src.database.config import get_db
from ..schemas.authentication import LoginModel
from ..user import _delete_user, _get_user_by_id, _update_user, _create_new_user

logger = getLogger(__name__)

user_route = APIRouter(prefix='/user', tags=['user'])


@user_route.post("/login", response_model=ShowUser)
async def login_user(body: LoginModel, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await login_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_route.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_route.delete("/", response_model=DeleteUserResponse)
async def delete_user(
        user_id: UUID, db: AsyncSession = Depends(get_db)
) -> DeleteUserResponse:
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_route.get("/", response_model=ShowUser)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user


@user_route.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
        user_id: UUID, body: UpdateUserRequest, db: AsyncSession = Depends(get_db)):
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, db=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)
