# Phase 2 - SQLite CRUD

Progress hari ini: Database & Table, INSERT, add_note(), SELECT,
get_notes()

## 1. SQLite & Koneksi Database

```
import sqlite3

connection = sqlite3.connect("notes.db")
cursor = connection.cursor()
```

Pemahaman: - sqlite3.connect() → membuka atau membuat database
SQLite. - connection → koneksi ke database. - connection.cursor() →
membuat cursor untuk menjalankan SQL. - cursor.execute() → menjalankan
perintah SQL.

### Struktur:

ai-study-notes-assistant/
├── app/
│   └── database/
│       └── database.py
├── notes.db
└── ...

## 2. Membuat Tabel notes
```
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    created_at TEXT,
    updated_at TEXT
);
```

Pemahaman: - id → identitas setiap row. - PRIMARY KEY → identitas
utama. - AUTOINCREMENT → SQLite memberikan ID otomatis. - title dan
content → data note. - created_at dan updated_at → waktu note.


## 3. INSERT --- Memasukkan Data

Dipahami bahwa Python dan SQL adalah dua bahasa berbeda. Ekspresi
Python di dalam string SQL tidak otomatis dieksekusi sebagai Python.

Timestamp dibuat terlebih dahulu:
```
created_at = str(datetime.datetime.now())
updated_at = str(datetime.datetime.now())
```
Kemudian digunakan dengan placeholder:
```
VALUES (?, ?, ?, ?)
```
Setelah INSERT, perubahan disimpan dengan:
```
connection.commit()
```
execute() menjalankan operasi SQL, sedangkan commit() menyimpan
perubahan data.

## 4. Fungsi add_note()
```
def add_note(title, content):

    created_at = str(datetime.datetime.now())
    updated_at = str(datetime.datetime.now())

    cursor.execute(
        """
        INSERT INTO notes(title, content, created_at, updated_at)
        VALUES(?, ?, ?, ?)
        """,
        (
            title,
            content,
            created_at,
            updated_at,
        ),
    )

    connection.commit()
``` 
Alur:

add_note()
    ↓
buat timestamp
    ↓
INSERT ke SQLite
    ↓
commit()

Fungsi sudah diuji dan data berhasil masuk ke database.

## 5. SELECT --- Mengambil Data
```
result = cursor.execute("""
    SELECT * FROM notes
""")

rows = result.fetchall()
```

Pemahaman: - execute() → menjalankan query. - fetchall() → mengambil
seluruh hasil query. - rows → kumpulan seluruh row. - row → satu
row.

## 6. Memproses Setiap Row
```
for row in rows:
    print(row)
```
Setiap nilai dapat diakses menggunakan index:
```
row[0] → id
row[1] → title
row[2] → content
row[3] → created_at
row[4] → updated_at
```
Contoh:
```
row = (5, "Python", "Belajar function", "tanggal", "tanggal")

print(row[1])
print(row[2])
```
Hasil:
```
Python
Belajar function
```
## 7. Fungsi get_notes()
```
def get_notes():
    result = cursor.execute("""
        SELECT * FROM notes
    """)

    rows = result.fetchall()
    return rows
```
Penggunaan:
```
rows = get_notes()

for row in rows:
    print(row)
```
Alur:
```
get_notes()
    ↓
execute SELECT
    ↓
fetchall()
    ↓
rows
    ↓
return rows
```
Konsepnya sama dengan get_notes() pada Phase 1, tetapi sekarang sumber
data adalah SQLite, bukan list Python.

## 8. Perbedaan Phase 1 dan Phase 2

Phase 1
```
Python
   ↓
List
   ↓
Note Object
```
Phase 2
```
Python
   ↓
SQL
   ↓
SQLite
   ↓
Row
```
Konsep penting:
```
rows → kumpulan row
row  → satu row
row[index] → nilai dalam row
```
## 9. SELECT * vs Kolom Spesifik

Untuk latihan digunakan:
```
SELECT * FROM notes;
```
Jika hanya membutuhkan title dan content:
```
SELECT title, content FROM notes;
```
Prinsip:

SQL menentukan data apa yang diambil; Python menentukan bagaimana
data hasil query diproses.

## 10. Duplicate Note

Jika menjalankan:
```
add_note("Math", "Algebra")
add_note("Math", "Algebra")
```
maka saat ini akan dibuat dua row berbeda.

Alasannya: - Belum ada validasi duplicate title. - title belum dibuat
UNIQUE. - SQLite memberikan id berbeda untuk setiap row.

Untuk scope proyek saat ini, validasi duplicate title belum ditambahkan
agar tidak menambah kompleksitas sebelum diperlukan.