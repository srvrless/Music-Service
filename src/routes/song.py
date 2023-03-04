from uuid import UUID

from fastapi import APIRouter, UploadFile, File, Form
from fastapi import Depends
from fastapi import HTTPException
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import get_db
from src.modules.image import upload_image
from src.modules.song import create_new_song, delete_sing, get_song_by_id_, upload_song, song_insert_to_liked
from src.schemas.song import DeleteSongResponse, LikedSong, LikedSongModel
from src.schemas.song import ShowSong
from src.schemas.song import SongCreate

song_router = APIRouter(prefix='/song', tags=['song'])

directory_name = "web/static/image"


@song_router.post("/alb", response_model=SongCreate)
async def create_song(title: str = Form(...),
                      creator: str = Form(...), image_file: UploadFile = File(...),
                      sound_file: UploadFile = File(...),
                      db: AsyncSession = Depends(get_db)):
    try:
        # if is_song(song_file.filename):
        upload_song(directory_name, sound_file)
        upload_image(directory_name, image_file)

        return await create_new_song(title, creator, song_file=sound_file.filename, img_file=image_file.filename, db=db)
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


@song_router.get("/", response_model=ShowSong)
async def get_song_by_id(song_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowSong:
    song = await get_song_by_id_(song_id, db)
    if song is None:
        raise HTTPException(
            status_code=404, detail=f"song with id {song_id} not found."
        )
    return song


@song_router.post("liked_song", response_model=LikedSong)
async def add_song_to_liked(song: LikedSongModel, db: AsyncSession = Depends(get_db)) -> ShowSong:
    user_id = song.user_id
    song_id = song.song_id
    song = await song_insert_to_liked(user_id, song_id, db)
    x = 'neverless'
    if song is None:
        raise HTTPException(
            status_code=404, detail=f"song with id {x} not found."
        )
    return song
