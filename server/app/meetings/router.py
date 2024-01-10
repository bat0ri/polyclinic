from fastapi import APIRouter, Depends, HTTPException
from app.meetings.repository import MeetRepo 
from auth.security import JWTBearer, get_current_user
from app.meetings.schemas import CreateMeeting, DropMeeting
from auth.models import User
from app.meetings.model import Meeting 

meeting_route = APIRouter()

@meeting_route.post("/create")
async def create_new_meeting(
    meeting_data: CreateMeeting,
    repo: MeetRepo = Depends(MeetRepo),
    current_user: User = Depends(get_current_user)
):

    existing_meetings = await repo.get_by_doctor_and_time(
        doctor_id=meeting_data.doctor_id,
        meet_date=meeting_data.meet_date
    )

    if existing_meetings:
        return {"detail": "У этого врача уже есть запись на это время."}

    new_meeting = Meeting(
        pacient_id=current_user.id,
        meet_date=meeting_data.meet_date,
        doctor_id=meeting_data.doctor_id,
        doctor_username=meeting_data.doctor_username
    )

    created_meeting = await repo.insert(new_meeting)
    await repo.close()

    return created_meeting

@meeting_route.get("/list")
async def get_all_my_meeting(
    repo: MeetRepo = Depends(MeetRepo),
    current_user: User = Depends(get_current_user)
):
    return await repo.get_by_user_uuid(current_user.id)

@meeting_route.delete("/delete")
async def drop_meeting_by_id(
    meet: DropMeeting,
    repo: MeetRepo = Depends(MeetRepo)
):
    try:
        await repo.drop(meet.id)
        await repo.close()
        return HTTPException(status_code=200, detail=f"Встреча {meet.id} удалена")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"{e}")

# spisok zapiseyi