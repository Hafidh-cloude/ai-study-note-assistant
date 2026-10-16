from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import get_notes, add_note, update_note, delete_note
from app.services.note_service import (
    delete_note_service,
    get_notes_service,
    create_note_service,
    summary_note_service,
    update_note_service,
)
from app.services.ai_service import ask_ai
from app.services.note_service import ask_note_service
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteUpdate(BaseModel):
    content: str


class Prompt(BaseModel):
    prompt: str


class NoteQuestion(BaseModel):
    question: str


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


@app.post("/ai/test")
def post_ai_endpoint(prompt: Prompt):
    try:
        return {
            "answer": ask_ai(prompt.prompt),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# @app.get("/test/ask-note")
# def test_ask_note():
#     return {
#         "prompt": ask_note_service(
#             1,
#             "Apa isi catatan tersebut?",
#         )
#     }


@app.post("/notes/{note_id}/ask")
def ask_note_endpoint(note_id: int, note: NoteQuestion):
    try:
        answer = ask_note_service(note_id, note.question)

        if not answer:
            raise HTTPException(
                status_code=404,
                detail="ID tidak ditemukan",
            )

        return {
            "answer": answer,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.post("/notes/{note_id}/summary")
def summary_note_endpoint(note_id: int):
    try:
        summary = summary_note_service(note_id)

        if not summary:
            raise HTTPException(
                status_code=404,
                detail="ID tidak ditemukan",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
    return {
        "summary": summary,
    }
