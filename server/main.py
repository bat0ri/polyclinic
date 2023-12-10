import uvicorn
from fastapi import FastAPI
from auth.router import user_route
from app.diagnoses.router import diagnose_route


app = FastAPI(
        title='Polyclinic',
        description='CRUD for medical models'
    )


app.include_router(user_route, prefix='/auth', tags=['JWT-Authentication'])

app.include_router(diagnose_route, prefix='/diagnose', tags=["Diagnose"])


