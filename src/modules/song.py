from typing import Union
from uuid import UUID
from src.schemas.song import SongModel
from src.schemas.song import SongCreate
from src.serializer.dal_song import SongDAL


async def create_new_song(body: SongCreate, db) -> SongModel:
    async with db as session:
        async with session.begin():
            song_dal = SongDAL(session)
            song = await song_dal.create_song(
                name=body.name,
                creator=body.creator,
                song_file=body.song_file,
                song_status=body.song_status,
                verified=body.verified
            )
            return SongModel(
                name=song.name,
                creator=body.creator,
                song_file=song.song_file,
            )


async def delete_sing(song_id, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            song_dal = SongDAL(session)
            deleted_song_id = await song_dal.delete_song(
                song_id=song_id,
            )
            return deleted_song_id


async def get_song_by_id_(song_id, db) -> Union[SongModel, None]:
    async with db as session:
        async with session.begin():
            song_dal = SongDAL(session)
            song = await song_dal.get_song_by_id(
                song_id=song_id,
            )
            if song is not None:
                return SongModel(
                    name=song.name,
                    creator=song.creator,
                    song_file=song.song_file,
                )