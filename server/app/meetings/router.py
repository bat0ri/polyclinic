from fastapi import APIRouter, Depends, HTTPException
from app.meetings.repository import MeetRepo 
from auth.security import JWTBearer, get_current_user
from app.meetings.schemas import CreateMeeting, DropMeeting
from auth.models import User
from app.meetings.model import Meeting 
from app.meetings.service import create_meeting




meeting_route = APIRouter()



@meeting_route.post("/create")
async def create_new_meeting(
    meeting_data: CreateMeeting,
    repo: MeetRepo = Depends(MeetRepo),
    current_user: User = Depends(get_current_user)
):
    res = await create_meeting(meeting_data, repo, current_user)
    return res




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