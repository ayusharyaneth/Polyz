import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db import Database
from utils.logger import logger
from services.health_service import HealthService
from config.settings import BOT_ADMIN_ID, ALERT_CHANNEL_ID, TELEGRAM_BOT_TOKEN
from aiohttp import ClientSession

async def send_alert(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": ALERT_CHANNEL_ID, "text": message}
    async with ClientSession() as session:
        await session.post(url, json=payload)

async def health_monitor_worker():
    await Database.connect()
    await send_alert("🚨 SYSTEM ALERT\n\nComponent: Workers\nStatus: System Startup")
    
    while True:
        try:
            db_lat = await HealthService.ping_db()
            if db_lat < 0 or db_lat > 500:
                await send_alert(f"🚨 SYSTEM ALERT\n\nComponent: Database\nError: High Latency or Disconnected ({db_lat}ms)")
            
            redis_lat = await HealthService.ping_redis()
            if redis_lat < 0 or redis_lat > 300:
                await send_alert(f"🚨 SYSTEM ALERT\n\nComponent: Redis\nError: High Latency or Disconnected ({redis_lat}ms)")
                
        except Exception as e:
            logger.error(f"Health Monitor Error: {e}")
            await send_alert(f"🚨 SYSTEM ALERT\n\nComponent: Health Monitor\nError: {str(e)}")
            
        await asyncio.sleep(60)

async def wallet_tracker_worker():
    # Placeholder for Web3 polling logic
    while True:
        await asyncio.sleep(10)

async def main():
    logger.info("Starting Workers...")
    await asyncio.gather(
        health_monitor_worker(),
        wallet_tracker_worker()
    )

if __name__ == "__main__":
    asyncio.run(main())
