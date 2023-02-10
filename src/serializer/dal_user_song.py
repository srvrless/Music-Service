from typing import Union
from uuid import UUID

from sqlalchemy import and_, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.song import Song


class SongDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def like_song(self, name: str, creator: str, song_status: str) -> Song:
        like_song = Song(
            name=name,
            creator=creator,
            song_status=song_status,
        )
        self.db_session.execute(like_song)
        await self.db_session.fethone()
        return like_song

    async def get_song_by_name(self, song_id: UUID) -> Union[Song, None]:
        query = select(Song)
        res = await self.db_session.execute(query)
        song_row = res.fetchone()
        if song_row is not None:
            return song_row[0]

    async def get_all_songs_in_likes(self, song_id: UUID) -> Union[Song, None]:
        query = select(Song).where(Song.is_liked == True)
        res = await self.db_session.execute(query)
        song_row = res.fetchall()
        if song_row is not None:
            return song_row[0]

    async def remove_song_in_likes(self, song_id: UUID) -> Union[UUID, None]:
        query = (
            delete(Song)
            .where(and_(Song.song_id == song_id, Song.is_liked == True))
            .returning(Song.song_id)
        )
        res = await self.db_session.execute(query)
        deleted_song_id_row = res.fetchone()
        if deleted_song_id_row is not None:
            return deleted_song_id_row[0]
