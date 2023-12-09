from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession
from auth.schema import CreateUser, GetUserByEmail, GetUserByUsername, LoginForm, TokenInfo
from auth.repository import UserRepo
from config import get_async_session
from auth.hashing import BcryptHasher
from auth.security import encode_jwt, decode_jwt, JWTBearer


user_route = APIRouter()

@user_route.post('/register')
async def register(user: CreateUser, session: AsyncSession = Depends(get_async_session)):
    repository = UserRepo(session)
    new_user = await repository.insert_new_user(user_data=user)
    await repository.close()
    return new_user

@user_route.get("/users")
async def all_users(session: AsyncSession = Depends(get_async_session)):
    repository = UserRepo(session)
    users = await repository.get_all_users()
    await repository.close()
    return users


@user_route.post("/login")
async def login_token(response: Response,
                        data: OAuth2PasswordRequestForm = Depends(),
                        session: AsyncSession = Depends(get_async_session)):
    repository = UserRepo(session=session)
    _user = await repository.get_user_by_username(data.username)
    await repository.close()
    if _user:
        if not BcryptHasher.verify_password(data.password, _user.hash_password):
            return {"status": "неправильный пароль"}
        else:
            payload = {"sub": _user.username, "email": _user.email}
            token = encode_jwt(payload=payload)
            response.set_cookie(key="access_token", value=token)
            return TokenInfo(
                access_token=token,
                token_type= "Bearer"
            )
    return {"status" : 500}

@user_route.get("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

@user_route.get("/protected", dependencies=[Depends(JWTBearer())])
async def all_users_with_token(session: AsyncSession = Depends(get_async_session)):
    repository = UserRepo(session)
    users = await repository.get_all_users()
    await repository.close()
    return users