# src/controllers/wallet_controller.py
from src.database.db import db_instance

async def add_target_wallet(user_id: int, address: str, label: str):
    await db_instance.db.target_wallets.update_one(
        {"user_id": user_id, "address": address},
        {"$set": {"label": label}},
        upsert=True
    )
