import datetime
import time


class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()


def add_note(title, content):
    new_note = Note(title, content)
    notes.append(new_note)


def get_notes():
    return notes


def update_note(title, new_content):
    for note in notes:
        if note.title == title:
            note.content = new_content
            note.updated_at = datetime.datetime.now()


def delete_note(title):
    for note in notes:
        if note.title == title:
            notes.remove(note)


notes = []

add_note("Math", "Geometry")
add_note("Computer", "Python")

time.sleep(2)

update_note("Math", "Algebra")
update_note("Computer", "AI")

delete_note("Computer")
result = get_notes()

for note in result:
    print(note.title + note.content)
    print(f"Waktu dibuat: {note.created_at}")
    print(f"Waktu update: {note.updated_at}")
