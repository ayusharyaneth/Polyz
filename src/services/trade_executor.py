# src/services/trade_executor.py
import asyncio
from src.database.db import db_pool
from src.services.polymarket_client import PolymarketClient
from src.services.risk_manager import RiskManager
from src.utils.retry import network_retry
from src.utils.logger import get_logger
from src.telegram.bot import send_alert

logger = get_logger(__name__)

class TradeExecutor:
    async def process_pending_trades(self):
        while True:
            try:
                trades = await db_pool.fetch("SELECT * FROM trades WHERE status = 'PENDING'")
                for trade in trades:
                    await self.execute_trade(trade)
            except Exception as e:
                logger.error("Trade executor loop error", error=str(e))
            await asyncio.sleep(2)

    @network_retry
    async def execute_trade(self, trade):
        user_id = trade['user_id']
        try:
            if not await RiskManager.validate_trade(user_id, trade['token_id'], float(trade['size']), 0.5): # mock price 0.5
                await db_pool.execute("UPDATE trades SET status = 'REJECTED_RISK' WHERE id = $1", trade['id'])
                await send_alert(user_id, f"⚠️ Risk Violation on Token {trade['token_id'][:6]}")
                return

            client = PolymarketClient(user_id)
            await client.initialize()
            
            # In a real scenario, fetch orderbook to determine precise price.
            # Using mock 0.5 for structural completeness.
            price = 0.5 
            
            res = await client.submit_order(trade['token_id'], trade['side'], price, float(trade['size']))
            
            await db_pool.execute("UPDATE trades SET status = 'EXECUTED', price = $2 WHERE id = $1", trade['id'], price)
            await send_alert(user_id, f"📈 Trade Copied! {trade['side']} {trade['size']} of {trade['token_id'][:6]}")
            
        except Exception as e:
            logger.error("Execution failed", trade_id=trade['id'], error=str(e))
            await db_pool.execute("UPDATE trades SET status = 'FAILED' WHERE id = $1", trade['id'])
            await send_alert(user_id, f"🚨 Execution Failed: {str(e)}")
            await send_alert(settings.ERROR_DUMP_CHAT_ID, f"🚨 BOT ERROR\nModule: Trade Executor\nTrade ID: {trade['id']}\nError: {str(e)}")
