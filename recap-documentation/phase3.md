# Phase 3: FastAPI & REST API

## Tujuan

Phase 3 berfokus pada pembangunan REST API menggunakan FastAPI dan penghubungannya dengan SQLite melalui Service Layer.

## Arsitektur:
```
Client
   ↓
FastAPI (main.py)
   ↓
Service Layer (note_service.py)
   ↓
Database (database.py)
   ↓
SQLite
```
## Pembagian tanggung jawab:
```
main.py → HTTP/API: endpoint, request, response, status code.

note_service.py → proses atau logika aplikasi terkait Note.

database.py → akses SQLite/SQL.
```
### Task 3.1 — GET /

Membuat aplikasi FastAPI dasar:
```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_note():
    return {"message": "Berhasil!"}
```
Server dijalankan dengan:
```
uv run uvicorn app.main:app --reload
```
Endpoint diuji melalui Swagger /docs.

**Konsep**: FastAPI() membuat aplikasi, decorator @app.get() membuat endpoint, dan Uvicorn menjalankan aplikasi.

### Task 3.2 — GET /notes

Endpoint digunakan untuk mengambil seluruh note dari SQLite.

Perbedaan penting:
```
get_notes
```
hanya merujuk ke function, sedangkan:
```
get_notes()
```
menjalankan function.

**Masalah SQLite thread**

Terjadi error sqlite3.ProgrammingError karena koneksi SQLite dibuat pada satu thread lalu digunakan pada thread lain.

Untuk project pembelajaran ini digunakan:
```
connection = sqlite3.connect(
    "notes.db",
    check_same_thread=False
)
```
Ini merupakan solusi sederhana untuk project ini, bukan pola universal untuk semua aplikasi.

### Task 3.3 — POST /notes

Request body menggunakan Pydantic:
```
class NoteCreate(BaseModel):
    title: str
    content: str
```
Endpoint menerima NoteCreate, kemudian meneruskan title dan content ke database.

**Konsep:**

- Pydantic memvalidasi dan menstrukturkan request body.

- note.title dan note.content berasal dari request body.

- NoteCreate merupakan model request body, bukan model database.

### Task 3.4 — PUT /notes/id

Path parameter digunakan untuk menentukan note yang di-update.

Contoh:
```
PUT /notes/5
```
Model request:
```
class NoteUpdate(BaseModel):
    content: str
```
note_id berasal dari URL/path parameter, sedangkan note.content berasal dari request body.

note_id tidak perlu dimasukkan ke NoteUpdate karena ID sudah tersedia sebagai path parameter.

### Task 3.5 — DELETE /notes/id

Database menggunakan:
```
DELETE FROM notes
WHERE id = ?
```
Untuk satu parameter SQL digunakan tuple satu elemen:
```
(note_id,)
```
Koma diperlukan agar Python mengenalinya sebagai tuple satu elemen.

### Task 3.6 — Error Handling

Untuk mengetahui apakah UPDATE atau DELETE benar-benar mengenai data, digunakan:
```
connection.commit()
return cursor.rowcount
```
Makna:
```
rowcount == 1 → satu baris terkena operasi.
rowcount == 0 → tidak ada baris yang cocok dengan WHERE.
```
Untuk ID yang tidak ditemukan:
```
raise HTTPException(
    status_code=404,
    detail="ID tidak ditemukan",
)
```
Status yang dipahami:

- 200 OK → operasi berhasil.

- 404 Not Found → resource tidak ditemukan.

- 400 Bad Request → request tidak valid.

### Task 3.7 — Structured Response

Response DELETE dirapikan menjadi:
```
return {
    "message": "Berhasil Dihapus!",
    "note_id": note_id,
}
```
Tujuannya agar response lebih konsisten dan informatif.

### Task 3.8 — Service Layer

Sebelum Service Layer:
```
main.py
   ↓
database.py
```
Setelah Service Layer:
```
main.py
   ↓
note_service.py
   ↓
database.py
```
Contoh DELETE:
```
def delete_note_service(note_id):
    result = delete_note(note_id)

    if result == 0:
        return False

    return True
```
main.py menangani HTTP:
```
result = delete_note_service(note_id)

if not result:
    raise HTTPException(
        status_code=404,
        detail="ID tidak ditemukan",
    )
```
Intinya:

- main.py → komunikasi HTTP.

- note_service.py → proses/logika aplikasi.

- database.py → akses SQLite/SQL.

Service tidak selalu harus memiliki logika kompleks. GET misalnya cukup:
```
def get_notes_service():
    return get_notes()
```
Service Layer untuk CRUD

Semua operasi CRUD kemudian melewati service:
```
GET
main.py → get_notes_service() → get_notes() → database

POST
main.py → create_note_service(title, content) → add_note() → database

PUT
main.py → update_note_service(note_id, content) → update_note() → database

DELETE
main.py → delete_note_service(note_id) → delete_note() → database
```
main.py tidak lagi mengakses fungsi database secara langsung untuk operasi CRUD yang sudah memiliki service.

Error Handling PUT
```
update_note() juga mengembalikan rowcount:

connection.commit()
return cursor.rowcount
```
Service:
```
def update_note_service(note_id, content):
    result = update_note(note_id, content)

    if result == 0:
        return False

    return True
```
Endpoint kemudian mengubah False menjadi HTTP 404.


Basic API Testing

Testing otomatis sederhana dibuat menggunakan Python dan requests.

Instalasi:
```
uv add requests
```
File:
```
tests/
└── test_api.py
```
Contoh:
```
import requests

response = requests.get(
    "http://127.0.0.1:8000/notes"
)

assert response.status_code == 200

print("GET /notes berhasil")
```
assert menyimpan expected behavior.

- Jika expected 200 dan actual 200 → test lulus.

- Jika expected 200 tetapi actual 500 → assert gagal.

Testing otomatis melengkapi manual testing melalui Swagger dan berguna untuk memastikan behavior tetap benar setelah perubahan kode.

Test yang Berhasil

GET
```
GET /notes
Expected: 200
Result: PASS
```
DELETE — ID tidak ditemukan
```
DELETE /notes/999999
Expected: 404
Result: PASS
```
POST
```
POST /notes
Expected: 200
Result: PASS
```
PUT
```
PUT /notes/1
Expected: 200
Result: PASS
```
ID yang digunakan harus merupakan ID yang memang ada di database.

**Hasil Quiz Phase 3**

Quiz terdiri dari 10 soal.

Nilai akhir: 9.25 / 10

**Materi:**

- Path parameter.
- Request body dan Pydantic.
- return.
- rowcount.
- HTTP status code.
- Service Layer.
- Function vs function call.
- return False.
- API testing.

**Alur Client → FastAPI → Service → Database → SQLite.**

*Kesalahan utama berupa ketelitian istilah, bukan konsep inti.*


**PHASE 3 —** ***SELESAI***

**CRUD:**
```
GET    /notes              ✓
POST   /notes              ✓
PUT    /notes/{id}         ✓
DELETE /notes/{id}         ✓
```
**Error handling:**
```
DELETE ID tidak ditemukan → 404 ✓
PUT ID tidak ditemukan    → 404 ✓
```
**Service Layer:**
```
GET    → service → database ✓
POST   → service → database ✓
PUT    → service → database ✓
DELETE → service → database ✓
```

**Basic API Testing:**
```
GET    → PASS ✓
POST   → PASS ✓
PUT    → PASS ✓
DELETE error case → PASS ✓
```