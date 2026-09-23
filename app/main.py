from fastapi import FastAPI, HTTPException
from app.database.database import get_notes, add_note, update_note, delete_note
from app.services.note_service import (
    delete_note_service,
    get_notes_service,
    create_note_service,
    update_note_service,
)
from pydantic import BaseModel

app = FastAPI()


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    content: str


# @app.get("/")
# def get_endpoint():
#     return {"Message": "Berhasil Terhubung!"}


@app.get("/notes")
def get_note_endpoint():
    return get_notes_service()


@app.post("/notes")
def create_note(note: NoteCreate):
    create_note_service(note.title, note.content)

    return {"Message": "Create Berhasil"}


@app.put("/notes/{note_id}")
def update_note_endpoint(note_id: int, note: NoteUpdate):
    result = update_note_service(note_id, note.content)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="ID tidak ditemukan",
        )
    return {
        "note_id": note_id,
        "content": note.content,
    }


@app.delete("/notes/{note_id}")
def delete_note_endpoint(note_id: int):
    result = delete_note_service(note_id)
    if result == 0:
        raise HTTPException(
            status_code=404,
            detail="ID tidak ditemukan",
        )
    return {
        "message": "Berhasil Dihapus!",
        "note_id": note_id,
    }
