from app.services.note_service import ask_note_service, summary_note_service

# def test_ask_note():
#     note_id = 1
#     question = "Apa isi catatan ini?"
#     answer = ask_note_service(note_id, question)
#     print(answer)


def test_summary_note():
    note_id = 10
    summary = summary_note_service(note_id)
    print(summary)


# test_ask_note()
test_summary_note()
