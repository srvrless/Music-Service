# import uuid
#
# from pydantic import BaseModel
#
# from src import TunedModel
#
#
# class ShowSong(TunedModel):
#     song_id: uuid.UUID
#     name: str
#     creator: str
#     is_liked: bool
#
#
# class SongCreate(BaseModel):
#     name: str
#     creator: str
#
#
# class DeleteSongResponse(BaseModel):
#     deleted_song_id: uuid.UUID
#
#
# class UpdatedSongResponse(BaseModel):
#     updated_song_id: uuid.UUID
#
#
# class UpdateSongRequest(BaseModel):
#     name: Optional[constr(min_length=1)]
#     creator: Optional[constr(min_length=1)]
