
# Phase 5  AI Context, Q&A, and Summary

## Overview
Phase 5 merupakan tahap pengembangan fitur AI pada AI Study Notes
Assistant. Pada fase ini, aplikasi diintegrasikan dengan Groq LLM
untuk menjawab pertanyaan berdasarkan isi catatan pengguna dan
menghasilkan ringkasan catatan.

AI menggunakan konten note yang diambil dari database SQLite sebagai
konteks.

## Features
1. AI Question Answering (Q&A)
Menjawab pertanyaan pengguna berdasarkan isi note yang dipilih.

- Mengambil note berdasarkan ID.
- Menggunakan konten note sebagai context.
- Menggabungkan context dengan pertanyaan pengguna menjadi prompt.
- Mengirim prompt ke Groq LLM.
- Mengembalikan jawaban AI dalam format JSON.
2. AI Summary
Menghasilkan ringkasan dari isi note yang dipilih.

- Mengambil note berdasarkan ID.
- Menggunakan konten note sebagai context.
- Membuat prompt khusus untuk meringkas catatan.
- Mengirim prompt ke Groq LLM.
- Mengembalikan ringkasan dalam format JSON.
3. Error Handling
- 404 Not Found --- note dengan ID yang diminta tidak ditemukan.
- 500 Internal Server Error --- terjadi kesalahan ketika memproses
permintaan, termasuk kegagalan komunikasi dengan Groq.

## Technology Stack

Python --- bahasa pemrograman utama.
FastAPI --- membangun REST API.
SQLite --- menyimpan data catatan.
Groq API --- mengakses model bahasa besar (LLM).
Pydantic --- memvalidasi request body.
Requests --- digunakan untuk pengujian API.
Model Groq yang digunakan: qwen/qwen3.8-27b.

## System Architecture
```
Client / Swagger UI
        |
        v
     FastAPI
     main.py
        |
        v
  Note Service
 note_service.py
        |
        +------------------+
        |                  |
        v                  v
    SQLite             AI Service
   database.py        ai_service.py
                           |
                           v
                       Groq API
                           |
                           v
                      AI Response
```

## Application Workflow
### Question Answering
```
User Question + Note ID
          |
          v
Get Note from SQLite
          |
          v
Extract Note Content
          |
          v
Combine Context + Question
          |
          v
Send Prompt to Groq
          |
          v
Return AI Answer
```
### Summary
```
Note ID
   |
   v
Get Note from SQLite
   |
   v
Extract Note Content
   |
   v
Create Summary Prompt
   |
   v
Send Prompt to Groq
   |
   v
Return Summary
```

## API Endpoints
1. Ask a Question
Endpoint: POST /notes/{note_id}/ask

Menghasilkan jawaban berdasarkan konten note dan pertanyaan pengguna.

Request body:
```
{
  "question": "Apa isi catatan ini?"
}
```
Contoh response:
```
{
  "answer": "Berdasarkan catatan yang diberikan, ..."
}
```
2. Generate Summary
Endpoint: POST /notes/{note_id}/summary

Menghasilkan ringkasan berdasarkan konten note yang dipilih. Endpoint
ini tidak membutuhkan request body karena sistem mengambil konteks dari
note berdasarkan ID.
```
Contoh response:

{
  "summary": "Ringkasan dari isi catatan ..."
}
```
## HTTP Status Codes
Status Code Description

- 200 OK Permintaan berhasil diproses.
- 404 Not Found Note dengan ID yang diminta tidak
ditemukan.
- 500 Internal Server Error Terjadi kesalahan pada proses
  
backend atau layanan AI.

## Running the Application
Jalankan perintah berikut dari root project:
```
uv run uvicorn app.main:app --reload
```
Buka Swagger UI melalui:
```
http://127.0.0.1:8000/docs
```
Gunakan Swagger UI untuk mencoba endpoint Q&A dan Summary.
