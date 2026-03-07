import asyncpg
from config.settings import DATABASE_URL
from utils.logger import logger

class Database:
    _pool = None

    @classmethod
    async def connect(cls):
        if not cls._pool:
            cls._pool = await asyncpg.create_pool(DATABASE_URL)
            logger.info("Database connected")

    @classmethod
    async def get_pool(cls):
        if not cls._pool:
            await cls.connect()
        return cls._pool

    @classmethod
    async def fetch(cls, query, *args):
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            return await conn.fetch(query, *args)

    @classmethod
    async def execute(cls, query, *args):
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            return await conn.execute(query, *args)
