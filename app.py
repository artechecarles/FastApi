from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI(title="🎵Music API🎵 (Using Fast Api)", description="A simple API to manage music tracks")

class Album(BaseModel):
    id: str
    name: str
    release_date: datetime


class Song(BaseModel):
    id: str
    name: str
    duration: int
    album: Album

song_db = [
    Song(id=uuid.uuid4().hex, name="Imagine", duration=183, album=Album(id=uuid.uuid4().hex, name="Imagine", release_date=datetime(1971, 10, 11))),
    Song(id=uuid.uuid4().hex, name="Hey Jude", duration=431, album=Album(id=uuid.uuid4().hex, name="Hey Jude", release_date=datetime(1968, 8, 26))),
    Song(id=uuid.uuid4().hex, name="Bohemian Rhapsody", duration=354, album=Album(id=uuid.uuid4().hex, name="A Night at the Opera", release_date=datetime(1975, 11, 21)))
]

@app.get(path="/song")
async def get_song():
    return [song.dict() for song in song_db]
