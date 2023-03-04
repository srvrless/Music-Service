from typing import Union
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

# from src.models.playlist import PlayList
from src.models.liked_songs import LikedSong
from src.models.song import Song


class SongDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_song(self, title: str, creator: str, song_file: str, img_file: str):
        new_song = Song(
            title=title,
            creator=creator,
            song_file=song_file,
            img_file=img_file

        )
        self.db_session.add(new_song)
        await self.db_session.flush()
        return new_song

    async def get_song_by_name(self, song_id: UUID) -> Union[Song, None]:
        query = select(Song)
        res = await self.db_session.execute(query)
        song_row = res.fetchone()
        if song_row is not None:
            return song_row[0]

    async def get_song_by_id(self, song_id: UUID) -> Union[Song, None]:
        query = select(Song).where(Song.song_id == song_id)
        res = await self.db_session.execute(query)
        song_row = res.fetchone()
        if song_row is not None:
            return song_row[0]

    async def delete_song(self, song_id: UUID) -> Union[UUID, None]:
        query = (
            delete(Song)
            .where(Song.song_id == song_id)
            .returning(Song.song_id)
        )
        res = await self.db_session.execute(query)
        deleted_song_id_row = res.fetchone()
        if deleted_song_id_row is not None:
            return deleted_song_id_row[0]

    async def added_song_to_liked(self, user_id: UUID, song_id: UUID):
        query = LikedSong(
            user_id=user_id,
            song_id=song_id
        )
        self.db_session.add(query)
        await self.db_session.flush()
        return query
