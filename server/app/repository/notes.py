from app.repository.dal import BaseRepo
from app.models.note import Note



class NoteRepo(BaseRepo[Note]):
    model = Note

