# src/database/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DatabaseInstance:
    def __init__(self):
        self.client = None
        self.db = None

    async def initialize(self):
        try:
            self.client = AsyncIOMotorClient(settings.DATABASE_URL)
            # Defaulting to a database named 'polymarket'
            self.db = self.client.get_default_database("polymarket")
            await self.client.admin.command('ping')
            logger.info("MongoDB cluster connected successfully")
        except Exception as e:
            logger.error("Failed to connect to MongoDB", error=str(e))
            raise

db_instance = DatabaseInstance()
