from app.database.database import (
    delete_note,
    get_notes,
    add_note,
    update_note,
)


def delete_note_service(note_id):
    result = delete_note(note_id)

    if result == 0:
        return False
    return True


def get_notes_service():
    return get_notes()


def create_note_service(title, content):
    add_note(title, content)


def update_note_service(note_id, content):
    result = update_note(note_id, content)

    if result == 0:
        return False
    return True
