from auth.repository import UserRepo
from auth.schema import RegistrationUser, TokenInfo
from auth.models import User
from auth.hashing import BcryptHasher
from auth.security import encode_jwt, decode_jwt
from config import get_async_session
from fastapi import Depends, Response, Cookie, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from auth.schema import LoginForm, UserProfile
import jwt


async def registration(user: RegistrationUser, session: AsyncSession = Depends(get_async_session)):
    async with UserRepo(session) as repository:
        if await repository.check_new_email(user.email):
            raise HTTPException(
                status_code=400,
                detail="Email уже зарегистрирован"
            )
        new_user = User(
            username=user.username,
            hash_password=BcryptHasher.get_password_hash(user.password),
            email=user.email,
            roles=[user.roles]
        )
        new_user = await repository.insert_user(new_user)
        return new_user


async def refresh_token(refresh_token: str,
                        session: AsyncSession = Depends(get_async_session)):

    try:
        decoded = decode_jwt(refresh_token)

        if decoded.get("token_type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")
        
        async with UserRepo(session=session) as repository:
            user = await repository.get_user_by_username(decoded.get("sub"))
            if user:
                response = Response() 
                return await create_token(user=user, response=response),
            else:
                raise HTTPException(status_code=404, detail="Пользователя нет")   
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

async def refresh_token_from_cookie(request: Request, response: Response, session: AsyncSession = Depends(get_async_session)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not found in cookies")

    try:
        decoded = decode_jwt(refresh_token)

        if decoded.get("token_type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")

        async with UserRepo(session=session) as repository:
            user = await repository.get_user_by_username(decoded.get("sub"))
            if user:
                tokens_with_user =  await create_token(user=user, response=response)
                auth_response = {
                    "access_token": tokens_with_user.access_token,
                    "refresh_token": tokens_with_user.refresh_token,
                    "token_type": tokens_with_user.token_type,
                    "user": user,
                }
                response.set_cookie(key="refresh_token", value=tokens_with_user.refresh_token, httponly=True, max_age=3600 * 24 * 7,  samesite="None", secure=True)
                return auth_response
            else:
                raise HTTPException(status_code=404, detail="Пользователя нет")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


async def create_token(user: User, response: Response):
    payload = {
        "sub": user.username,
        "email": user.email,
        "roles": user.roles
    }
    access_token, refresh_token = encode_jwt(payload=payload)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer"
    )


async def login(response: Response,
                form_data: LoginForm,
                session: AsyncSession = Depends(get_async_session)):

    async with UserRepo(session=session) as repository:
        user = await repository.get_user_by_username(form_data.username)
        if user:
            if BcryptHasher.verify_password(form_data.password, user.hash_password):
                tokens_with_user =  await create_token(user=user, response=response)
                auth_response = {
                    "access_token": tokens_with_user.access_token,
                    "refresh_token": tokens_with_user.refresh_token,
                    "token_type": tokens_with_user.token_type,
                    "user": user,
                }
                response.set_cookie(key="refresh_token", value=tokens_with_user.refresh_token, httponly=True, max_age=3600 * 24 * 7,  samesite="None", secure=True)
                return auth_response
            else:
                raise HTTPException(status_code=400, detail="Неправильный пароль")
        else:
            raise HTTPException(status_code=404, detail="Пользователь с таким именем не существует")
