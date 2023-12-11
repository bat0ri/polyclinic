from pydantic import BaseModel, validator
from datetime import datetime, timezone


class CreateMeeting(BaseModel):
    meet_date: datetime

    @validator('meet_date')
    def remove_timezone_info(cls, value):
        return value.replace(tzinfo=None)

class DropMeeting(BaseModel):
    id: int
