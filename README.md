# 🎵 Music API (FastAPI Learning Project)

This project is a small example API developed as a learning exercise for the micro framework **FastAPI**. It allows you to manage songs and albums, demonstrating CRUD operations (create, read, update, delete) and the use of automatic documentation.

## Features

- Full CRUD for songs.
- Nested model for albums.
- Partial update of songs (PATCH).
- Automatic documentation and examples using FastAPI.
- No database: data is stored in memory.

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn

## Installation

```bash
pip install fastapi uvicorn
```

## Running

```bash
uvicorn app:app --reload
```

Then, access the interactive documentation at:  
[http://localhost:8000/docs](http://localhost:8000/docs)

## Notes

- This project is for educational purposes only and should not be used in production.
- Data will be lost when the application restarts.

---
Developed as a FastAPI learning exercise.
