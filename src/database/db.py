# src/database/db.py
import asyncpg
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DatabasePool:
    def __init__(self):
        self.pool = None

    async def initialize(self):
        try:
            self.pool = await asyncpg.create_pool(settings.DATABASE_URL)
            logger.info("Database pool initialized")
        except Exception as e:
            logger.error("Failed to initialize database", error=str(e))
            raise

    async def fetch(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)
            
    async def fetchrow(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

db_pool = DatabasePool()
