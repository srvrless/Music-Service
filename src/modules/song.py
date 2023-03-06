from time import strftime
from typing import Union
from uuid import UUID

from fastapi import UploadFile, HTTPException

from src.layouts.dal_song import SongDAL
from src.layouts.dal_favorite_song import FavoriteSongDAL
from src.schemas.song import ShowSong
from src.schemas.liked_song import LikedSongModel, ShowLikedSong
from sqlalchemy.ext.asyncio import AsyncSession


def is_song(filename: str) -> bool:
    valid_extensions = (".mp3", ".jpg", ".jpeg", ".png")
    return filename.endswith(valid_extensions)


def upload_song(directory_name: str, song: UploadFile):
    """Upload image with add datetime on root directory"""
    # if is_song(song.filename):
    timestr = strftime("%Y%m%d-%H%M%S")
    song_name = timestr + song.filename
    with open(f'{directory_name}/{song_name}', 'wb+') as song_file_upload:
        song_file_upload.write(song.file.read())
    return f"{directory_name}/{song_name}"
    # raise HTTPException(status_code=403, detail=f"Not valid type")


async def create_new_song(title, creator, song_file, img_file, db: AsyncSession):
    async with db as session:
        async with session.begin():
            song_dal = SongDAL(session)
            song = await song_dal.create_song(
                title=title,
                creator=creator,
                song_file=song_file,
                img_file=img_file
            )
            return ShowSong(
                title=title,
                creator=creator,
                song_file=song_file,
                img_file=img_file
            )


async def _delete_song(song_id, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            song_dal = SongDAL(session)
            deleted_song_id = await song_dal.delete_song(
                song_id=song_id,
            )
            return deleted_song_id


async def get_song_by_id_(song_id, db) -> Union[ShowSong, None]:
    async with db as session:
        async with session.begin():
            song_dal = SongDAL(session)
            song = await song_dal.get_song_by_id(
                song_id=song_id,
            )
            if song is not None:
                return ShowSong(
                    title=song.title,
                    creator=song.creator,
                    song_file=song.song_file
                )


# async def song_insert_playlist(song_id, db) -> Union[ShowSong, None]:
#     async with db as session:
#         async with session.begin():
#             song_dal = SongDAL(session)
#             song = await song_dal.get_song_by_id(
#                 song_id=song_id,
#             )
#             if song is not None:
#                 return ShowSong(
#                     name=song.name,
#                     creator=song.creator,
#                     song_file=song.song_file,
#                 )
async def song_insert_to_libary(user_id, song_id, db) -> LikedSongModel:
    async with db as session:
        async with session.begin():
            song_dal = FavoriteSongDAL(session)
            song = await song_dal.added_song_to_favorite(
                user_id=user_id,
                song_id=song_id
            )
            if song is not None:
                return LikedSongModel(
                    user_id=user_id,
                    song_id=song_id,
                )


async def get_all_songs_in_libary(db: AsyncSession)->ShowLikedSong:
    async with db as session:
        async with session.begin():
            song_dal = FavoriteSongDAL(session)
            return await song_dal.get_all_songs_in_libary()
