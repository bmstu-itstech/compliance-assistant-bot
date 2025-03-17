import logging

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker

from services.db.models import Base

logger = logging.getLogger(__name__)


async def create_db_pool(user, password, host, name, echo):
    engine = create_async_engine(
        f"postgresql+asyncpg://{user}:{password}@{host}:5432/{name}",
        echo=echo,
        future=True,
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    created_async_sessionmaker = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return created_async_sessionmaker
