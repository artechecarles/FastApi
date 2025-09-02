from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import Optional
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request

# Initialize Jinja2Templates
templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="🎵Music API🎵 (Using Fast Api)",
    description="Una API simple para gestionar canciones y álbumes de música. Permite crear, listar, actualizar y eliminar canciones, así como realizar actualizaciones parciales.",
    version="1.1.0"
)

class Album(BaseModel):
    id: str = Field(..., description="Identificador único del álbum", example="a1b2c3d4e5")
    name: str = Field(..., description="Nombre del álbum", example="Imagine")
    release_date: datetime = Field(..., description="Fecha de lanzamiento del álbum", example="1971-10-11T00:00:00")


class Song(BaseModel):
    id: str = Field(..., description="Identificador único de la canción", example="f6g7h8i9j0")
    name: str = Field(..., description="Nombre de la canción", example="Imagine")
    duration: int = Field(..., description="Duración de la canción en segundos", example=183)
    album: Album = Field(..., description="Álbum al que pertenece la canción")

# For PATCH: allow partial update
class SongPartialUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Nuevo nombre de la canción", example="Imagine (Remastered)")
    duration: Optional[int] = Field(None, description="Nueva duración en segundos", example=185)
    album: Optional[Album] = Field(None, description="Nuevo álbum")

song_db = [
    Song(id=uuid.uuid4().hex, name="Imagine", duration=183, album=Album(id=uuid.uuid4().hex, name="Imagine", release_date=datetime(1971, 10, 11))),
    Song(id=uuid.uuid4().hex, name="Hey Jude", duration=431, album=Album(id=uuid.uuid4().hex, name="Hey Jude", release_date=datetime(1968, 8, 26))),
    Song(id=uuid.uuid4().hex, name="Bohemian Rhapsody", duration=354, album=Album(id=uuid.uuid4().hex, name="A Night at the Opera", release_date=datetime(1975, 11, 21)))
]

def get_all_songs():
    return song_db


@app.get("/songs", response_class=HTMLResponse)
async def get_songs_html(request: Request):
    songs = get_all_songs()  # Assuming you have a function to fetch songs
    return templates.TemplateResponse("songs.html", {
        "request": request, 
        "songs": songs, 
        "title": "Song List"
    })

@app.get(
    path="/song",
    summary="Obtener canciones",
    description="Devuelve una lista de todas las canciones o una canción específica si se proporciona un ID.",
    response_model=list[Song]  # Cuando se retorna la lista
)
async def get_song(id: Optional[str] = None):
    if id is None:
        return song_db
    if (song := next(filter(lambda song: song.id == id, song_db), None)) is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

@app.post(
    path="/song",
    summary="Crear una canción",
    description="Agrega una nueva canción a la base de datos.",
    response_model=Song
)
async def create_song(song: Song):
    song_db.append(song)
    return song

@app.delete(
    path="/song/{id}",
    summary="Eliminar una canción",
    description="Elimina una canción de la base de datos por su ID."
)
async def delete_song(id: str):
    global song_db
    song_db = [song for song in song_db if song.id != id]
    return {"message": "Song deleted successfully"}


@app.put(
    path="/song/{id}",
    summary="Actualizar una canción",
    description="Reemplaza completamente una canción existente por su ID.",
    response_model=Song
)
async def update_song(id: str, updated_song: Song):
    for index, song in enumerate(song_db):
        if song.id == id:
            song_db[index] = updated_song
            return updated_song
    return {"error": "Song not found!"}

@app.patch(
    path="/song/{id}",
    summary="Actualizar parcialmente una canción",
    description="Actualiza parcialmente los campos de una canción existente por su ID.",
    response_model=Song
)
async def partial_update_song(id: str, updated_fields: SongPartialUpdate):
    for index, song in enumerate(song_db):
        if song.id == id:
            updated_song = song.copy(update=updated_fields.dict(exclude_unset=True))
            song_db[index] = updated_song
            return updated_song
    return {"error": "Song not found!"}
