import uvicorn
from fastapi import FastAPI
from auth.router import user_route
from app.diagnoses.router import diagnose_route
from app.notes.router import note_route
from app.meetings.router import meeting_route


app = FastAPI(
        title='Polyclinic',
        description='CRUD for medical models'
    )


app.include_router(user_route, prefix='/auth', tags=['JWT-Authentication routes'])

app.include_router(diagnose_route, prefix='/diagnose', tags=["Diagnose routes"])

app.include_router(note_route, prefix="/note", tags=["Note routes"])

app.include_router(meeting_route, prefix="/meeting", tags=["Meetings route"])


