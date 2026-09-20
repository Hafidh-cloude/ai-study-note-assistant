# Phase 2: SQLite CRUD

## Tujuan

Mengganti penyimpanan data dari Python list pada Phase 1 menjadi database SQLite dan mengimplementasikan CRUD menggunakan SQL secara langsung tanpa ORM.

### 1. Koneksi SQLite
```
import sqlite3

connection = sqlite3.connect("notes.db")
cursor = connection.cursor()
```
connection = koneksi ke database.
cursor = digunakan untuk menjalankan SQL.
sqlite3.connect() membuka koneksi dan dapat membuat notes.db jika belum ada.

### 2. Membuat Tabel
```
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    created_at TEXT,
    updated_at TEXT
);
```
Kolom:
```
id → ID unik otomatis.
title → judul.
content → isi.
created_at → waktu dibuat.
updated_at → waktu diperbarui.
```
### 3. INSERT — Create
```
cursor.execute(
    "INSERT INTO notes(title, content, created_at, updated_at) "
    "VALUES(?, ?, ?, ?)",
    (title, content, created_at, updated_at),
)

connection.commit()
```
? adalah placeholder parameter. Nilai diberikan terpisah dari SQL.

commit() menyimpan perubahan transaksi ke database dan digunakan setelah INSERT, UPDATE, atau DELETE.

### 4. SELECT — Read
```
result = cursor.execute("SELECT * FROM notes")
rows = result.fetchall()
```
fetchall() mengambil seluruh hasil query.

Jika row:
```
(3, "Python", "Belajar function", "tanggal1", "tanggal2")
```
maka:
```
row[0] → id
row[1] → title
row[2] → content
row[3] → created_at
row[4] → updated_at
```
rows = kumpulan seluruh baris, sedangkan row = satu baris.

### 5. get_notes()
```
def get_notes():
    result = cursor.execute("SELECT * FROM notes")
    rows = result.fetchall()
    return rows
```
Phase 1 mengambil data dari list Python. Phase 2 mengambil data dari database menggunakan SQL.

### 6. add_note()
```
def add_note(title, content):
    created_at = str(datetime.datetime.now())
    updated_at = str(datetime.datetime.now())

    cursor.execute(
        "INSERT INTO notes(title, content, created_at, updated_at) "
        "VALUES(?, ?, ?, ?)",
        (title, content, created_at, updated_at),
    )
    connection.commit()
```
Belum ada validasi judul duplikat, sehingga title yang sama dapat dibuat lebih dari sekali.

### 7. UPDATE
```
def update_note(title, new_content):
    updated_at = str(datetime.datetime.now())

    cursor.execute(
        "UPDATE notes "
        "SET content = ?, updated_at = ? "
        "WHERE title = ?",
        (new_content, updated_at, title),
    )
    connection.commit()
```
WHERE menentukan baris yang terkena UPDATE. Tanpa WHERE, seluruh baris dapat diperbarui.

Saat note di-update:
```
content berubah.

updated_at berubah.

created_at tetap.
```
### 8. DELETE
```
def delete_note(title):
    cursor.execute(
        "DELETE FROM notes WHERE title = ?",
        (title,),
    )
    connection.commit()
```
Detail Python penting:
```
(title)     # bukan tuple
(title,)    # tuple satu elemen
```
Koma membuatnya menjadi tuple.

Jika beberapa row memiliki title yang sama, implementasi saat ini akan menghapus semua row yang memenuhi WHERE title = ?.

### 9. Pola CRUD SQLite
```
Function
    ↓
cursor.execute(SQL, parameters)
    ↓
connection.commit()  ← untuk perubahan data
```
```
Create → INSERT
Read   → SELECT
Update → UPDATE
Delete → DELETE
```
### 10. Phase 1 vs Phase 2

**Phase 1**
```
notes.append(new_note)
```
Data disimpan di memory Python dan hilang ketika program berhenti.

**Phase 2**
```
cursor.execute(...)
connection.commit()
```
Data disimpan di notes.db sehingga dapat digunakan kembali.

Perubahan konsep:
```
Phase 1 → Python List → Object di memory
Phase 2 → SQLite      → Row di database
```
### 11. Status

✅ Database connection
✅ Membuat table
✅ INSERT
✅ SELECT
✅ UPDATE
✅ DELETE
✅ CRUD SQLite
✅ commit()
✅ Parameterized query
✅ rows dan row
✅ WHERE

#### Phase 2 — SQLite CRUD: ***SELESAI***