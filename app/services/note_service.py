from app.database.database import (
    delete_note,
    get_notes,
    add_note,
    update_note,
    get_note_by_id,
)

from app.services.ai_service import create_prompt, ask_ai, create_summary_prompt


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


def ask_note_service(note_id, question):
    by_id = get_note_by_id(note_id)

    if by_id is None:
        return False

    context = by_id[2]
    prompt = create_prompt(context, question)
    answer = ask_ai(prompt)
    return answer


def summary_note_service(note_id):
    by_id = get_note_by_id(note_id)

    if by_id is None:
        return False

    context = by_id[2]
    summary_prompt = create_summary_prompt(context)
    summary = ask_ai(summary_prompt)
    return summary
