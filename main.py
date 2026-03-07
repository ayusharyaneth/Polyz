import asyncio
from src.config.settings import settings
from src.database.db import db_instance  # <-- Changed this to db_instance
from src.database.migrations import run_migrations
from src.utils.logger import get_logger
from src.telegram.bot import start_bot
from src.workers.wallet_tracker import WalletTracker
from src.workers.trade_listener import TradeListener
from src.services.rpc_manager import rpc_manager
from src.services.health_service import HealthMonitor

logger = get_logger(__name__)

async def main():
    logger.info("Starting Polymarket Copy Trading Bot System...")
    
    # Initialize MongoDB
    await db_instance.initialize()  # <-- Changed this to db_instance
    await run_migrations()
    
    # Initialize RPC Manager
    await rpc_manager.initialize()

    # Start Health Monitor
    health_monitor = HealthMonitor()
    asyncio.create_task(health_monitor.start_monitoring())

    # Start Workers
    wallet_tracker = WalletTracker()
    asyncio.create_task(wallet_tracker.start())
    
    trade_listener = TradeListener()
    asyncio.create_task(trade_listener.start())

    # Start Telegram Bot (blocks)
    await start_bot()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("System shutting down...")
