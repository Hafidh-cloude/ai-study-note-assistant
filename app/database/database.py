import sqlite3
import datetime

connection = sqlite3.connect("notes.db")

cursor = connection.cursor()

cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title Text,
    content Text,
    created_at Text,
    updated_at Text
    )
""")


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


# for row in rows:
#     print(row[0])
#     print(row[1])
#     print(row[2])


def get_note():
    result = cursor.execute("""
    SELECT * FROM notes
    """)

    rows = result.fetchall()
    return rows


add_note("Python", "Belajar Function")
rows = get_note()

for row in rows:
    print(row)
