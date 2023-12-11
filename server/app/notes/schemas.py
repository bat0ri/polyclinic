from pydantic import BaseModel


class CreateNote(BaseModel):
    description: str
    diagnose_id: int | None