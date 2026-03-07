# src/services/trade_executor.py
import asyncio
from src.config.settings import settings
from src.database.db import db_instance
from src.services.polymarket_client import PolymarketClient
from src.services.risk_manager import RiskManager
from src.utils.retry import network_retry
from src.utils.logger import get_logger
from src.telegram.bot import send_alert

logger = get_logger(__name__)

class TradeExecutor:
    async def process_pending_trades(self):
        db = db_instance.db
        while True:
            try:
                trades = await db.trades.find({"status": "PENDING"}).to_list(None)
                for trade in trades:
                    await self.execute_trade(trade)
            except Exception as e:
                logger.error("Trade executor loop error", error=str(e))
            await asyncio.sleep(2)

    @network_retry
    async def execute_trade(self, trade):
        user_id = trade['user_id']
        trade_id = trade['_id']
        db = db_instance.db
        
        try:
            if not await RiskManager.validate_trade(user_id, trade['token_id'], float(trade['size']), 0.5):
                await db.trades.update_one({"_id": trade_id}, {"$set": {"status": "REJECTED_RISK"}})
                await send_alert(user_id, f"⚠️ Risk Violation on Token {trade['token_id'][:6]}")
                return

            client = PolymarketClient(user_id)
            await client.initialize()
            
            price = 0.5 
            
            res = await client.submit_order(trade['token_id'], trade['side'], price, float(trade['size']))
            
            await db.trades.update_one({"_id": trade_id}, {"$set": {"status": "EXECUTED", "price": price}})
            await send_alert(user_id, f"📈 Trade Copied! {trade['side']} {trade['size']} of {trade['token_id'][:6]}")
            
        except Exception as e:
            logger.error("Execution failed", trade_id=str(trade_id), error=str(e))
            await db.trades.update_one({"_id": trade_id}, {"$set": {"status": "FAILED"}})
            await send_alert(user_id, f"🚨 Execution Failed: {str(e)}")
            await send_alert(settings.ERROR_DUMP_CHAT_ID, f"🚨 BOT ERROR\nModule: Trade Executor\nTrade ID: {str(trade_id)}\nError: {str(e)}")
