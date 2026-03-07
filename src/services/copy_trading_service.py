# src/services/copy_trading_service.py
from src.utils.logger import get_logger
from src.database.db import db_pool
from src.services.polymarket_client import PolymarketClient
from src.services.risk_manager import RiskManager

logger = get_logger(__name__)

class CopyTradingEngine:
    @staticmethod
    async def process_detected_trade(target_address: str, token_id: str, amount: float, is_buy: bool):
        followers = await db_pool.fetch("SELECT user_id FROM target_wallets WHERE address = $1", target_address)
        
        side = "BUY" if is_buy else "SELL"
        
        for follower in followers:
            user_id = follower['user_id']
            settings = await db_pool.fetchrow("SELECT copy_percentage FROM bot_settings WHERE user_id = $1", user_id)
            if not settings:
                continue

            copy_pct = float(settings['copy_percentage']) / 100.0
            trade_size = amount * copy_pct

            # Assume market price fetching logic here via client
            client = PolymarketClient(user_id)
            await client.initialize()
            
            # Simple execution wrapper push to DB for queue
            await db_pool.execute(
                """INSERT INTO trades (user_id, target_address, token_id, side, size, price, status) 
                   VALUES ($1, $2, $3, $4, $5, 0, 'PENDING')""",
                user_id, target_address, token_id, side, trade_size
            )
            logger.info("Queued copy trade", user_id=user_id, size=trade_size)
