import uvicorn
from fastapi import FastAPI
from auth.router import user_route


app = FastAPI(
        title='Polyclinic',
        description='CRUD for medical models'
    )


app.include_router(user_route, prefix='/auth', tags=['auth'])


