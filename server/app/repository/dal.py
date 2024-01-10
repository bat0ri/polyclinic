from typing import Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from config import get_async_session
from sqlalchemy import select, delete, update

T = TypeVar('T')


class BaseRepo(Generic[T]):
    model: T
    session: AsyncSession

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def close(self):
        await self.session.close()

    async def insert(self, instance: T):
        self.session.add(instance)
        await self.session.commit()
        return instance

    async def get_all(self):
        q = select(self.model)
        exe = await self.session.execute(q)
        return exe.scalars().all()

    async def get_by_id(self, item_id: int):
        q = select(self.model).where(self.model.id==item_id)
        exe = await self.session.execute(q)
        return exe.scalar()

    async def drop(self, item_id: int):
        q = delete(self.model).filter(self.model.id==item_id)
        await self.session.execute(q)
        await self.session.commit()

    async def update(self, item_id: int, values: dict):
        q = update(self.model).where(self.model.id == item_id).values(values)
        await self.session.execute(q)
        await self.session.commit()


