import os
from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.song import SongModel
from src.schemas.song import SongCreate
from src.schemas.song import DeleteSongResponse
from src.database.config import get_db
from src.modules.song import create_new_song, delete_song, get_song_by_id

logger = getLogger(__name__)
song_route = APIRouter(prefix='/song', tags=['song'])


@song_route.post("/", response_model=SongModel)
async def create_song(body: SongCreate, db: AsyncSession = Depends(get_db),
                      Authorize: AuthJWT = Depends()) -> SongModel:
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    try:
        return await create_new_song(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@song_route.delete("/", response_model=DeleteSongResponse)
async def delete_song(song_id: UUID, db: AsyncSession = Depends(get_db)) -> DeleteSongResponse:
    deleted_song_id = await delete_song(song_id, db)
    if deleted_song_id is None:
        raise HTTPException(
            status_code=404, detail=f"song with id {song_id} not found."
        )
    return DeleteSongResponse(deleted_song_id=deleted_song_id)


@song_route.get("/", response_model=SongModel)
async def get_song_by_id(song_id: UUID, db: AsyncSession = Depends(get_db)) -> SongModel:
    song = await get_song_by_id(song_id, db)
    if song is None:
        raise HTTPException(
            status_code=404, detail=f"song with id {song_id} not found."
        )
    return song


@song_route.get("/gif")
async def images():
    out = []
    for filename in os.listdir("static/gif"):
        out.append({
            "name": filename.split(".")[0],
            "path": "/static/gif/" + filename
        })
    return out[0]
