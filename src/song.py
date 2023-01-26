import os
from logging import getLogger
from typing import Union
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.song import DeleteSongResponse
from src.models.song import ShowSong
from src.models.song import SongCreate
from src.serializer.dals_user import SongDAL
from src.database.config import get_db

logger = getLogger(__name__)

song_route = APIRouter(prefix='/song', tags=['song'])


async def _create_new_song(body: SongCreate, db) -> ShowSong:
    async with db as session:
        async with session.begin():
            song_dal = SongDAL(session)
            song = await song_dal.create_song(
                name=body.name,
                creator=body.creator,
            )
            return ShowSong(
                song_id=song.song_id,
                name=song.name,
                creator=song.creator,
                is_liked=song.is_liked,
            )


async def _delete_song(song_id, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            song_dal = SongDAL(session)
            deleted_song_id = await song_dal.delete_song(
                song_id=song_id,
            )
            return deleted_song_id


async def _get_song_by_id(song_id, db) -> Union[ShowSong, None]:
    async with db as session:
        async with session.begin():
            song_dal = SongDAL(session)
            song = await song_dal.get_song_by_id(
                song_id=song_id,
            )
            if song is not None:
                return ShowSong(
                    song_id=song.song_id,
                    name=song.name,
                    creator=song.creator,
                    is_liked=song.is_liked,
                )



