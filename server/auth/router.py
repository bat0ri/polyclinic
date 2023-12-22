from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordBearer,  HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from auth.schema import (CreateUser, GetUserByEmail, GetUserByUsername, 
                        LoginForm, TokenInfo, RegistrationUser)

from auth.repository import UserRepo
from config import get_async_session
from auth.hashing import BcryptHasher
from auth.security import encode_jwt, decode_jwt, JWTBearer, get_current_user
from auth.service import registration, login, refresh_token, refresh_token_from_cookie


user_route = APIRouter()


@user_route.post('/registration')
async def register_user_new(user: RegistrationUser, session: AsyncSession = Depends(get_async_session)):
    return await registration(user=user, session=session)


@user_route.post("/login")
async def login_user(response: Response,
    form_data: LoginForm,
                     session: AsyncSession = Depends(get_async_session)):
    return await login(response=response, form_data=form_data,
                        session=session)

@user_route.get("/refresh")
async def refresh_tokens(refresh: str,session: AsyncSession = Depends(get_async_session)):
    return await refresh_token(refresh_token=refresh, session=session)

@user_route.get("/refresh_token")
async def refresh_tokens_from_cookie(request: Request, response: Response, session: AsyncSession = Depends(get_async_session)):
    return await refresh_token_from_cookie(request, response, session)

@user_route.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token", secure=True, httponly=True, samesite="None")
    return {"message": "Logged out successfully"}

@user_route.get("/profile")
async def get_profile(user = Depends(get_current_user)):
    return user

@user_route.get("/protected", dependencies=[Depends(JWTBearer())])
async def all_users_with_token(session: AsyncSession = Depends(get_async_session)):
    repository = UserRepo(session)
    users = await repository.get_all_doctors()
    await repository.close()
    return users

