from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import POSTGRES_DSN_ASYNC
from .base import Base

DATABASE_URL = POSTGRES_DSN_ASYNC

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#     async with engine.begin() as conn:
#         yield conn


async def init_models():
    async with engine.begin() as conn:
        # раскоментировать строку ниже, чтобы удалить таблицу для обновления структуры
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
