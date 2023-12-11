from fastapi import APIRouter, Depends, HTTPException
from app.notes.repository import NoteRepo
from config import get_async_session
from auth.security import RoleBasedJWTBearer, get_current_user
from app.notes.schemas import CreateNote
from auth.models import User
from app.notes.model import Note


note_route = APIRouter()



@note_route.post("/create", dependencies=[Depends(RoleBasedJWTBearer())])
async def create_new_note(
    note_data: CreateNote,
    repo: NoteRepo = Depends(NoteRepo),
    current_user: User = Depends(get_current_user)
):

    if not current_user.is_doctor:
        raise HTTPException(status_code=403, detail="Permission denied. Only doctors can create notes.")

    new_note = Note(
        doctor_id=current_user.id, 
        description=note_data.description,
        diagnose=note_data.diagnose_id 
    )

    created_note = await repo.insert(new_note)
    await repo.close()

    return created_note

