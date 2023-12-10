from auth.repository import UserRepo
from auth.schema import RegistrationUser, TokenInfo
from auth.models import User
from auth.hashing import BcryptHasher
from auth.security import encode_jwt
from config import get_async_session
from fastapi import Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from auth.schema import LoginForm


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
        )
        new_user = await repository.insert_user(new_user)
        return new_user


async def create_token(user: User, response: Response) -> TokenInfo:
    payload = {
        "sub": user.username,
        "email": user.email
        }
    token = encode_jwt(payload=payload)
    response.set_cookie(key="access_token", value=token)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )


async def login(form_data: LoginForm,
                session: AsyncSession = Depends(get_async_session)):

    async with UserRepo(session=session) as repository:
        user = await repository.get_user_by_username(form_data.username)
        if user:
            if BcryptHasher.verify_password(form_data.password, user.hash_password):
                response = Response()
                return await create_token(user=user, response=response)
            else:
                raise HTTPException(status_code=400, detail="Неправильный пароль")
        else:
            raise HTTPException(status_code=404, detail="Пользователь с таким именем не существует")
