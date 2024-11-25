from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
