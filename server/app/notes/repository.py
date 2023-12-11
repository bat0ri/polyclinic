from app.dal import BaseRepo
from app.notes.model import Note



class NoteRepo(BaseRepo[Note]):
    model = Note

