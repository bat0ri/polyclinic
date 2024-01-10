from pydantic import BaseModel, validator
from datetime import datetime, timezone
from uuid import UUID


class CreateMeeting(BaseModel):
    meet_date: datetime
    doctor_id: UUID
    doctor_username: str | None

    @validator('meet_date')
    def remove_timezone_info(cls, value):
        return value.replace(tzinfo=None)

class DropMeeting(BaseModel):
    id: int
