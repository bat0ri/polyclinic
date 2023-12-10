import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv


load_dotenv()

DB_URL = os.getenv('DB_CONFIG')

engine = create_async_engine(DB_URL, future=True, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session



# JWT Configuration

PUBLIC_KEY = 'PUBLIC_KEY'
PRIVATE_KEY_PATN = os.getenv("PRIVATE_KEY_PATN")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
