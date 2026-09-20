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


def update_note(title, new_content):
    updated_at = str(datetime.datetime.now())
    cursor.execute(
        """
    UPDATE notes
    SET content = ?, updated_at = ?
    WHERE title = ?
    """,
        (
            new_content,
            updated_at,
            title,
        ),
    )
    connection.commit()


def delete_note(title):
    cursor.execute(
        """
        DELETE FROM notes
        WHERE title = ?
    """,
        (title,),
    )
    connection.commit()


# add_note("Informatics", "Artificial Intelligence")
# update_note("Math", "Algebra")
delete_note("Biologsy")
rows = get_note()

for row in rows:
    print(row)
