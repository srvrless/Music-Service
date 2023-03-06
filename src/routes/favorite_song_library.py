from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.config import get_db
from src.models.liked_songs import LikedSong
from src.modules.song import get_all_songs_in_libary, song_insert_to_libary
from src.schemas.liked_song import LikedSongModel, ShowLikedSong
from src.modules.user import oauth2_scheme

libary_router = APIRouter(prefix='/libary', tags=['libary'])


@libary_router.post('/')
async def libary_insert(song: LikedSongModel, db: AsyncSession = Depends(get_db),
                        token: str = Depends(oauth2_scheme)) -> ShowLikedSong:
    user_id = song.user_id
    song_id = song.song_id
    try:
        song = await song_insert_to_libary(user_id, song_id, db)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Auth")
    if song is None:
        raise HTTPException(
            status_code=404, detail=f"song with id {song_id} not found."
        )
    return song


@libary_router.get("/sniger")
async def get_all(db: AsyncSession = Depends(get_db)):
    try:
        result = await get_all_songs_in_libary(db)
        if result is None:
            return f"Your libary is empty"
    except Exception as error:
        raise HTTPException(status_code=404, detail="Not found")
    return result
