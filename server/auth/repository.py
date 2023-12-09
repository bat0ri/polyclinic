from auth.models import User
from auth.schema import CreateUser, GetUserByEmail, GetUserByUsername
from config import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select, delete, update
from auth.hashing import BcryptHasher
import datetime


class UserRepo():

    def __init__(self, session: AsyncSession):
        self.session = session

    async def close(self):
        await self.session.close()

    async def insert_new_user(self, user_data: CreateUser):
        new_user = User(
            username=user_data.username,
            hash_password=BcryptHasher.get_password_hash(user_data.hash_password),
            email=user_data.email,
        )
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_all_users(self):
        query = select(User).filter(User.is_active==True)
        user_list = await self.session.execute(query)
        return user_list.scalars().all()

    async def get_user_by_email(self, email: GetUserByEmail):
        query = select(User).where(User.email==email)
        user = await self.session.execute(query)
        return user.scalars().first()

    async def get_user_by_username(self, username: GetUserByUsername):
        query = select(User).where(User.username==username)
        user = await self.session.execute(query)
        return user.scalars().first()

    async def delete_user(self, username: GetUserByUsername):
        query = update(User).where(User.username==username).values(is_active=False)
        await self.session.execute(query)
        await self.session.commit()
        return await self.get_user_by_username(username=username)

    async def drop_user(self, username: str):
        delete_query = delete(User).where(User.username == username)
        await self.session.execute(delete_query)
        await self.session.commit()
        
    