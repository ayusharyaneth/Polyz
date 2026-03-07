# src/workers/trade_listener.py
import asyncio
import json
import redis.asyncio as redis
from src.config.settings import settings
from src.services.copy_trading_service import CopyTradingEngine
from src.services.trade_executor import TradeExecutor
from src.utils.logger import get_logger

logger = get_logger(__name__)

class TradeListener:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)
        self.executor = TradeExecutor()

    async def start(self):
        logger.info("Trade listener started")
        asyncio.create_task(self.executor.process_pending_trades())
        
        pubsub = self.redis.pubsub()
        await pubsub.subscribe("new_trades")
        
        async for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                await CopyTradingEngine.process_detected_trade(
                    data['address'], data['token_id'], data['amount'], data['is_buy']
                )
