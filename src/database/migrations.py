# src/database/migrations.py
import pymongo
from src.database.db import db_instance
from src.utils.logger import get_logger

logger = get_logger(__name__)

async def run_migrations():
    logger.info("Setting up MongoDB indexes...")
    db = db_instance.db
    
    await db.users.create_index("_id")
    await db.bot_settings.create_index("user_id", unique=True)
    await db.target_wallets.create_index(
        [("user_id", pymongo.ASCENDING), ("address", pymongo.ASCENDING)], 
        unique=True
    )
    logger.info("MongoDB indexes ready.")
