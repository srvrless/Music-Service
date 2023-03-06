from typing import Union, Sequence
from uuid import UUID

from sqlalchemy import select, delete, update, Row
from sqlalchemy.engine.result import _TP
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def get_songs_by_name(self, title: str) -> Sequence[Row[_TP]]:
        query = select(Song).where(Song.title == title)
        res = await self.db_session.execute(query)
        song_row = res.fetchall()
        if song_row:
            return song_row

    async def get_song_by_id(self, song_id: UUID) -> Union[Song, None]:
        query = select(Song).where(Song.song_id == song_id)
        res = await self.db_session.execute(query)
        song_row = res.fetchone()
        if song_row is not None:
            return song_row[0]

    async def _delete_song(self, song_id: UUID) -> Union[UUID, None]:
        query = (
            delete(Song)
            .where(Song.song_id == song_id)
            .returning(Song.song_id)
        )
        res = await self.db_session.execute(query)
        deleted_song_id_row = res.fetchone()
        if deleted_song_id_row is not None:
            return deleted_song_id_row[0]

    async def _update_song(self, song_id: UUID, title: str, creator: str, song_file: str, img_file: str) -> Union[
        UUID, None]:
        query = (
            update(Song)
            .where(Song.song_id == song_id)
            .values(title=title,
                    creator=creator,
                    song_file=song_file,
                    img_file=img_file)
            .returning(Song)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row:
            return update_user_id_row[0]
