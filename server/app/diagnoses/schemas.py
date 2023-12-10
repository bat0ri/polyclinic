from pydantic import BaseModel


class CreateDiagnose(BaseModel):
    name: str
    description: str | None