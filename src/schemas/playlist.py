import uuid
from pydantic import BaseModel


class Playlist(BaseModel):
    song_id: uuid.UUID
