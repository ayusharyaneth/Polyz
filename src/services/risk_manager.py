# src/services/risk_manager.py
from src.database.db import db_pool
from src.utils.logger import get_logger

logger = get_logger(__name__)

class RiskManager:
    @staticmethod
    async def validate_trade(user_id: int, token_id: str, size: float, price: float) -> bool:
        settings = await db_pool.fetchrow("SELECT * FROM bot_settings WHERE user_id = $1", user_id)
        if not settings:
            return False

        notional_value = size * price
        
        if notional_value > settings['max_trade_size']:
            logger.warning(f"Trade rejected: Max trade size exceeded ({notional_value} > {settings['max_trade_size']})")
            return False

        daily_trades = await db_pool.fetchrow(
            "SELECT COALESCE(SUM(size * price), 0) as total FROM trades WHERE user_id = $1 AND timestamp::date = CURRENT_DATE AND status = 'failed'", 
            user_id
        )
        
        if daily_trades['total'] + notional_value > settings['max_daily_loss']:
            logger.warning("Trade rejected: Max daily loss risk exceeded")
            return False

        return True
