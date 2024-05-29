from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)


Base = declarative_base(cls=PreBase)

database_engine = create_async_engine(settings.database_url, echo=True)

AsyncSessionFactory = sessionmaker(
    database_engine, expire_on_commit=False, class_=AsyncSession
)


async def get_async_session() -> AsyncSession:
    """Генератор сессий для работы с базой данных."""
    async with AsyncSessionFactory() as async_session:
        yield async_session
