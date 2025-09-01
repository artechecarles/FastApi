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
async def get_song(id:str):
    if (song := next (filter(lambda song: song.id == id, song_db), None)) is None:
        return song_db
    return song

@app.post(path="/song")
async def create_song(song: Song):
    song_db.append(song)
    return song

@app.delete(path="/song/{id}")
async def delete_song(id: str):
    global song_db
    song_db = [song for song in song_db if song.id != id]
    return {"message": "Song deleted successfully"}


@app.put(path="/song/{id}")
async def update_song(id: str, updated_song: Song):
    for index, song in enumerate(song_db):
        if song.id == id:
            song_db[index] = updated_song
            return updated_song
    return {"error": "Song not found!"}

@app.patch(path="/song/{id}")
async def partial_update_song(id: str, updated_fields: dict):
    for index, song in enumerate(song_db):
        if song.id == id:
            updated_song = song.copy(update=updated_fields)
            song_db[index] = updated_song
            return updated_song
    return {"error": "Song not found!"}
