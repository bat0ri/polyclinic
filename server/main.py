import uvicorn
from fastapi import FastAPI
from auth.router import user_route
from app.router.diagnose import diagnose_route
from app.router.note import note_route
from app.router.meet import meeting_route
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
        title='Polyclinic',
        description='CRUD for medical models'
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_route, prefix='/auth', tags=['JWT-Authentication routes'])

app.include_router(diagnose_route, prefix='/diagnose', tags=["Diagnose routes"])

app.include_router(note_route, prefix="/note", tags=["Note routes"])

app.include_router(meeting_route, prefix="/meeting", tags=["Meetings route"])


