import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.cache import get_redis
from src.database import async_session


async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_cache() -> redis.Redis.pipeline:
    return await get_redis()
