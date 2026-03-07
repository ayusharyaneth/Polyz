# src/services/risk_manager.py
from datetime import datetime, time as dtime
from src.database.db import db_instance
from src.utils.logger import get_logger

logger = get_logger(__name__)

class RiskManager:
    @staticmethod
    async def validate_trade(user_id: int, token_id: str, size: float, price: float) -> bool:
        db = db_instance.db
        settings = await db.bot_settings.find_one({"user_id": user_id})
        if not settings:
            return False

        notional_value = size * price
        
        if notional_value > settings.get('max_trade_size', 1000):
            logger.warning(f"Trade rejected: Max trade size exceeded ({notional_value} > {settings['max_trade_size']})")
            return False

        today_start = datetime.combine(datetime.utcnow().date(), dtime.min)
        pipeline = [
            {"$match": {"user_id": user_id, "timestamp": {"$gte": today_start}, "status": "FAILED"}},
            {"$group": {"_id": None, "total": {"$sum": {"$multiply": ["$size", "$price"]}}}}
        ]
        
        result = await db.trades.aggregate(pipeline).to_list(1)
        daily_loss = result[0]['total'] if result else 0
        
        if daily_loss + notional_value > settings.get('max_daily_loss', 500):
            logger.warning("Trade rejected: Max daily loss risk exceeded")
            return False

        return True
