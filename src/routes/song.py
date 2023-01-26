import os
from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.song import DeleteSongResponse
from src.models.song import ShowSong
from src.models.song import SongCreate
from src.database.config import get_db
from src.song import _create_new_song, _delete_song, _get_song_by_id

logger = getLogger(__name__)

song_route = APIRouter()


@song_route.post("/", response_model=ShowSong)
async def create_song(body: SongCreate, db: AsyncSession = Depends(get_db)) -> ShowSong:
    try:
        return await _create_new_song(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@song_route.delete("/", response_model=DeleteSongResponse)
async def delete_song(
        song_id: UUID, db: AsyncSession = Depends(get_db)
) -> DeleteSongResponse:
    deleted_song_id = await _delete_song(song_id, db)
    if deleted_song_id is None:
        raise HTTPException(
            status_code=404, detail=f"song with id {song_id} not found."
        )
    return DeleteSongResponse(deleted_song_id=deleted_song_id)


@song_route.get("/", response_model=ShowSong)
async def get_song_by_id(song_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowSong:
    song = await _get_song_by_id(song_id, db)
    if song is None:
        raise HTTPException(
            status_code=404, detail=f"song with id {song_id} not found."
        )
    return song


@song_route.get("/gif")
def images():
    out = []
    for filename in os.listdir("static/gif"):
        out.append({
            "name": filename.split(".")[0],
            "path": "/static/gif/" + filename
        })
    return out
