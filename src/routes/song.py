import os
from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import get_db
from src.modules.song import create_new_song, delete_sing, get_song_by_id_
from src.modules.user import oauth2_scheme
from src.schemas.song import DeleteSongResponse
from src.schemas.song import SongCreate
from src.schemas.song import SongModel

logger = getLogger(__name__)
song_router = APIRouter(prefix='/song', tags=['song'])


@song_router.post("/", response_model=SongModel)
async def create_song(body: SongCreate, db: AsyncSession = Depends(get_db)) -> SongModel:
    # try:
    #     Authorize.jwt_required()
    #
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    try:
        return await create_new_song(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@song_router.delete("/", response_model=DeleteSongResponse)
async def delete_song(song_id: UUID, db: AsyncSession = Depends(get_db)) -> DeleteSongResponse:
    deleted_song_id = await delete_sing(song_id, db)
    if deleted_song_id is None:
        raise HTTPException(
            status_code=404, detail=f"song with id {song_id} not found."
        )
    return DeleteSongResponse(deleted_song_id=deleted_song_id)


@song_router.get("/", response_model=SongModel)
async def get_song_by_id(song_id: UUID, db: AsyncSession = Depends(get_db)) -> SongModel:
    song = await get_song_by_id_(song_id, db)
    if song is None:
        raise HTTPException(
            status_code=404, detail=f"song with id {song_id} not found."
        )
    return song


