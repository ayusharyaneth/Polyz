# src/services/copy_trading_service.py
from datetime import datetime
from src.utils.logger import get_logger
from src.database.db import db_instance
from src.services.polymarket_client import PolymarketClient

logger = get_logger(__name__)

class CopyTradingEngine:
    @staticmethod
    async def process_detected_trade(target_address: str, token_id: str, amount: float, is_buy: bool):
        db = db_instance.db
        followers = await db.target_wallets.find({"address": target_address}).to_list(None)
        
        side = "BUY" if is_buy else "SELL"
        
        for follower in followers:
            user_id = follower['user_id']
            settings = await db.bot_settings.find_one({"user_id": user_id})
            if not settings:
                continue

            copy_pct = float(settings.get('copy_percentage', 100)) / 100.0
            trade_size = amount * copy_pct

            await db.trades.insert_one({
                "user_id": user_id,
                "target_address": target_address,
                "token_id": token_id,
                "side": side,
                "size": trade_size,
                "price": 0,
                "status": "PENDING",
                "timestamp": datetime.utcnow()
            })
            logger.info("Queued copy trade", user_id=user_id, size=trade_size)
