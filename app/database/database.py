import sqlite3
import datetime

connection = sqlite3.connect("notes.db", check_same_thread=False)

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


def get_notes():
    result = cursor.execute("""
    SELECT * FROM notes
    """)

    rows = result.fetchall()
    return rows


def update_note(note_id, new_content):
    updated_at = str(datetime.datetime.now())
    cursor.execute(
        """
    UPDATE notes
    SET content = ?, updated_at = ?
    WHERE id = ?
    """,
        (
            new_content,
            updated_at,
            note_id,
        ),
    )
    connection.commit()
    return cursor.rowcount


def delete_note(note_id):
    cursor.execute(
        """
        DELETE FROM notes
        WHERE id = ?
    """,
        (note_id,),
    )
    connection.commit()
    return cursor.rowcount


# add_note("Informatics", "Artificial Intelligence")
# update_note("Math", "Algebra")
delete_note("Biologsy")
rows = get_notes()

# for row in rows:
#     print(row)
