# Implements redis cache for the application
# Do the connection to the redis server and cache the data

import redis.asyncio as redis

from src.config import Config


async def get_redis() -> redis.Redis:
    return await redis.from_url(Config().REDIS_URL)
