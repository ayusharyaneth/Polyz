# src/controllers/settings_controller.py
from src.database.db import db_pool

async def update_copy_percentage(user_id: int, percentage: float):
    await db_pool.execute("UPDATE bot_settings SET copy_percentage = $1 WHERE user_id = $2", percentage, user_id)
