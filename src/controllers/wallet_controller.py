# src/controllers/wallet_controller.py
from src.database.db import db_pool

async def add_target_wallet(user_id: int, address: str, label: str):
    await db_pool.execute(
        "INSERT INTO target_wallets (user_id, address, label) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING",
        user_id, address, label
    )
