async def delete_song(self, song_id: UUID) -> Union[UUID, None]:
    query = (
        delete(Song)
        .where(and_(Song.song_id == song_id, Song.is_liked == False))
        .returning(Song.song_id)
    )
    res = await self.db_session.execute(query)
    deleted_song_id_row = res.fetchone()
    if deleted_song_id_row is not None:
        return deleted_song_id_row[0]
