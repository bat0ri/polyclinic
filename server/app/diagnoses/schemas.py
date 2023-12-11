from pydantic import BaseModel


class CreateDiagnose(BaseModel):
    name: str
    description: str | None

class ReadDiagnose(BaseModel):
    name: str

class UpdateDiagnose(BaseModel):
    name: str | None
    description: str | None