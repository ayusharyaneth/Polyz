# src/controllers/trade_controller.py
from src.database.db import db_instance

async def get_positions(user_id: int):
    return await db_instance.db.positions.find({"user_id": user_id}).to_list(length=None)
