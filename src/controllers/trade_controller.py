# src/controllers/trade_controller.py
from src.database.db import db_pool

async def get_positions(user_id: int):
    return await db_pool.fetch("SELECT * FROM positions WHERE user_id = $1", user_id)
