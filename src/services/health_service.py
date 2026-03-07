# src/services/health_service.py
import time
import asyncio
import aiohttp
import redis.asyncio as redis
from src.database.db import db_instance
from src.services.rpc_manager import rpc_manager
from src.config.settings import settings

class HealthMonitor:
    @staticmethod
    async def ping_all():
        stats = {}
        
        # MongoDB
        start = time.perf_counter()
        try:
            await db_instance.client.admin.command('ping')
            stats['MongoDB'] = f"{(time.perf_counter() - start) * 1000:.0f} ms"
        except:
            stats['MongoDB'] = "Down"

        # Redis
        start = time.perf_counter()
        try:
            r = redis.from_url(settings.REDIS_URL)
            await r.ping()
            stats['Redis'] = f"{(time.perf_counter() - start) * 1000:.0f} ms"
            await r.aclose()
        except:
            stats['Redis'] = "Down"

        # Polymarket
        start = time.perf_counter()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{settings.POLYMARKET_HOST}/time") as resp:
                    if resp.status == 200:
                        stats['Polymarket API'] = f"{(time.perf_counter() - start) * 1000:.0f} ms"
                    else:
                        stats['Polymarket API'] = "Error"
        except:
            stats['Polymarket API'] = "Down"

        # RPC
        if rpc_manager.active_rpc:
            stats['RPC'] = f"{rpc_manager.latencies.get(rpc_manager.active_rpc, 0):.0f} ms"
        else:
            stats['RPC'] = "Down"

        return stats

    async def start_monitoring(self):
        while True:
            await asyncio.sleep(60)
