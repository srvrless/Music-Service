from typing import Union
from uuid import UUID

from sqlalchemy import and_, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.liked_songs import LikedSong
from src.models.song import Song


class FavoriteSongDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_favorite_song_by_title(self, song_id: UUID) -> Union[Song, None]:
        query = select(LikedSong).where(LikedSong.song_id == song_id)
        res = await self.db_session.execute(query)
        song_row = res.fetchone()
        if song_row:
            return song_row[0]

    async def get_all_songs_in_libary(self):
        query = select(LikedSong)
        res = await self.db_session.execute(query)
        songs = res.fetchall()
        if songs:
            return [song[0] for song in songs]

    async def remove_song_from_favorites(self, user_id, song_id) -> Union[UUID, None]:
        song = delete(LikedSong).where(and_(LikedSong.user_id == user_id, LikedSong.song_id == song_id))
        await self.db_session.execute(song)
        await self.db_session.flush()
        return song

    async def added_song_to_favorite(self, user_id: UUID, song_id: UUID) -> Union[UUID, None]:
        song = select(LikedSong).where(and_(LikedSong.user_id == user_id, LikedSong.song_id == song_id))
        query = LikedSong(
            user_id=user_id,
            song_id=song_id
        )
        if song:
            await self.remove_song_from_favorites(user_id, song_id)
        self.db_session.add(query)
        await self.db_session.flush()
        return query
    