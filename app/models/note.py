import datetime


class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()


note1 = Note("Exam", "Study Math")
note2 = Note("Final Exam", "Study Computer")

print(note1.title)
print(note1.content)
print(f"Waktu dibuat: {note1.created_at}")
print(f"Waktu update: {note1.updated_at}")
print(note2.title)
print(note2.content)
print(f"Waktu dibuat: {note2.created_at}")
print(f"Waktu update: {note2.updated_at}")
