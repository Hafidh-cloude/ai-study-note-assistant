# Phase 4: LLM Integration


Target Phase 4 adalah membuat aplikasi dapat berkomunikasi dengan LLM melalui API. Pada project ini digunakan Groq API dengan model qwen/qwen3.8-27b.

### 1. Tujuan Phase 4

Alur utama:
```
Python
   ↓
Groq API
   ↓
LLM
   ↓
Response
   ↓
Jawaban AI
```
Setelah dihubungkan dengan FastAPI:
```
Client / Swagger
      ↓
POST /ai/test
      ↓
main.py
      ↓
ai_service.py
      ↓
Groq API
      ↓
LLM
      ↓
Jawaban AI
      ↓
Client
```
Phase 4 berfokus pada integrasi LLM. Penggunaan isi Note sebagai context untuk AI dilakukan pada Phase 5.

### 2. Instalasi Groq SDK

Karena project menggunakan uv:
```
uv add groq
```
Groq SDK digunakan untuk membuat client dan mengirim request ke Groq API.

### 3. API Key dengan .env

API key disimpan di:
```
.env
```
Format:
```
GROQ_API_KEY=gsk_xxxxxxxxx
```
Tidak menggunakan tanda kutip.

File .env ditambahkan ke .gitignore:
```
.env
```
Tujuannya agar API key tidak ikut ter-push ke GitHub.

### 4. Membaca API Key dari Python

Library:
```
uv add python-dotenv
```
Kode dasar:
```
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
```
Pengecekan:
```
if api_key:
    print("API key berhasil terbaca")
else:
    print("API key tidak terbaca")
```
Yang dipahami:
```
load_dotenv() memuat variabel dari .env.

os.getenv("GROQ_API_KEY") mengambil environment variable.
```
API key tidak dicetak ke terminal.

### 5. Membuat Groq Client
```
from groq import Groq

client = Groq(api_key=api_key)
```
client adalah object yang digunakan Python untuk berkomunikasi dengan Groq API menggunakan API key.

Alur:
```
.env
 ↓
GROQ_API_KEY
 ↓
api_key
 ↓
Groq(api_key=api_key)
 ↓
client
```
### 6. Request ke LLM

Request dibuat dengan:
```
response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
)
```
Yang dipahami:

- model menentukan model LLM.
- messages berupa list.
- Message berupa dictionary.
- role="user" menunjukkan pesan user.
- content berisi prompt.

Saat dijalankan:
```
Python
 ↓
client
 ↓
Groq API
 ↓
Qwen LLM
 ↓
response
```
Hasil request disimpan dalam response.

### 7. Memahami Response

Struktur penting response:
```
ChatCompletion
 ├── choices
 │    └── message
 │         └── content
```
Jawaban AI diambil dengan:
```
response.choices[0].message.content
```
Alurnya:
```
response
 ↓
choices
 ↓
[0]
 ↓
message
 ↓
content
 ↓
jawaban AI
```
choices merupakan list sehingga [0] mengambil pilihan pertama.

### 8. ai_service.py

File:
```
app/services/ai_service.py
```
Fungsi utama:
```
def ask_ai(prompt):
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content
```
Tanggung jawab ask_ai():

- menerima prompt.
- mengirim prompt ke Groq.
- menerima response.
- mengambil content.
- mengembalikan jawaban dengan return.

Contoh:
```
answer = ask_ai("Jelaskan apa itu Python")
print(answer)
```
### 9. Integrasi dengan FastAPI

Model request:
```
class Prompt(BaseModel):
    prompt: str
```
Request body:
```
{
    "prompt": "Jelaskan apa itu Python"
}
```
Endpoint:
```
POST /ai/test
```
Endpoint:
```
@app.post("/ai/test")
def post_ai_endpoint(prompt: Prompt):
    return {
        "answer": ask_ai(prompt.prompt)
    }
```
Alur:
```
JSON request
    ↓
Prompt
    ↓
prompt.prompt
    ↓
ask_ai(prompt.prompt)
    ↓
Groq API
    ↓
LLM
    ↓
answer
    ↓
FastAPI response
```
Response:
```
{
    "answer": "Python adalah ..."
}
```
### 10. Error Handling

Di ai_service.py, error diteruskan:
```
def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content

    except Exception as e:
        raise e
```
ai_service.py tidak menggunakan HTTPException karena tanggung jawabnya adalah komunikasi dengan LLM.

Di main.py, error diubah menjadi HTTP response:
```
@app.post("/ai/test")
def post_ai_endpoint(prompt: Prompt):
    try:
        return {
            "answer": ask_ai(prompt.prompt)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
```
Alur:
```
Groq error
   ↓
ai_service.py
   ↓
raise e
   ↓
main.py
   ↓
except Exception
   ↓
HTTPException
   ↓
HTTP 500
   ↓
Client
```
Pengujian dengan model yang tidak tersedia menghasilkan error 404 model_not_found, dan error berhasil ditangkap serta dikembalikan FastAPI.

### 11. Structured Response

Response string:
```
"Python adalah ..."
```
diubah menjadi dictionary:
```
return {
    "answer": ask_ai(prompt.prompt)
}
```
FastAPI mengembalikannya sebagai JSON:
```
{
    "answer": "Python adalah ..."
}
```
### 12. Testing Phase 4

Test menggunakan requests:
```
response = requests.post(
    "http://127.0.0.1:8000/ai/test",
    json={
        "prompt": "Jelaskan apa itu Python"
    }
)

assert response.status_code == 200
```
Response JSON diambil dengan:
```
response.json()
```
Hasil:
```
{
    "answer": "Python adalah bahasa pemrograman ..."
}
```
Pengecekan key:
```
assert "answer" in response.json()
```
Hasil testing:
```
GET /notes berhasil
DELETE /notes/{id} - ID tidak ditemukan: berhasil
POST /notes berhasil
PUT /notes/{id} berhasil
{'answer': 'Python adalah ...'}
```
Berarti:

✅ HTTP status = 200
✅ Response berupa JSON
✅ Key "answer" tersedia

13. Arsitektur Phase 4

                  Client / Swagger
                         │
                         ▼
                  POST /ai/test
                         │
                         ▼
                     main.py
                 HTTP/API Layer
                         │
                         ▼
                  ask_ai(prompt)
                         │
                         ▼
                  ai_service.py
                    AI Service
                         │
                         ▼
                    Groq Client
                         │
                         ▼
                     Groq API
                         │
                         ▼
                    Qwen LLM
                         │
                         ▼
                     Response
                         │
                         ▼
          response.choices[0].message.content
                         │
                         ▼
                  main.py / JSON
                         │
                         ▼
              {"answer": "..."}

### 14. Hal yang Dipahami

Phase 4 berhasil melatih:

- Groq SDK
- API key dengan .env
- python-dotenv
- os.getenv()
- Groq client
- request ke LLM
- model dan messages
- struktur response API
- nested object/list
- response.choices[0].message.content
- fungsi ask_ai(prompt)
return
- integrasi service dengan FastAPI
- request body Pydantic
- JSON response
- try/except
- raise
- HTTPException
- HTTP 500
- testing dengan requests
- response.json()
- assertion