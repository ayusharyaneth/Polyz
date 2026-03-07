import time
import asyncio
from aiohttp import ClientSession
from database.db import Database
from web3 import AsyncWeb3
from config.settings import TELEGRAM_BOT_TOKEN
import redis.asyncio as redis
from config.settings import REDIS_URL

class HealthService:
    @staticmethod
    async def ping_rpc(rpc_url: str) -> float:
        if not rpc_url: return -1
        try:
            w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc_url))
            start = time.perf_counter()
            await w3.eth.block_number
            return (time.perf_counter() - start) * 1000
        except:
            return -1

    @staticmethod
    async def ping_db() -> float:
        try:
            start = time.perf_counter()
            await Database.execute("SELECT 1")
            return (time.perf_counter() - start) * 1000
        except:
            return -1

    @staticmethod
    async def ping_redis() -> float:
        try:
            r = redis.from_url(REDIS_URL)
            start = time.perf_counter()
            await r.ping()
            await r.close()
            return (time.perf_counter() - start) * 1000
        except:
            return -1

    @staticmethod
    async def ping_telegram() -> float:
        try:
            async with ClientSession() as session:
                start = time.perf_counter()
                async with session.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe", timeout=5) as resp:
                    if resp.status == 200:
                        return (time.perf_counter() - start) * 1000
            return -1
        except:
            return -1
