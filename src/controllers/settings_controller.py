# src/controllers/settings_controller.py
from src.database.db import db_instance

async def update_copy_percentage(user_id: int, percentage: float):
    await db_instance.db.bot_settings.update_one(
        {"user_id": user_id}, 
        {"$set": {"copy_percentage": percentage}}
    )
