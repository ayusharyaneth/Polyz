# src/services/rpc_manager.py
import asyncio
import aiohttp
import time
from web3 import AsyncWeb3, AsyncHTTPProvider
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class RPCManager:
    def __init__(self):
        self.urls = settings.DEFAULT_RPC_URLS
        self.active_rpc = None
        self.latencies = {}

    async def initialize(self):
        await self.refresh_rpcs()
        asyncio.create_task(self._monitor_loop())

    async def _monitor_loop(self):
        while True:
            await asyncio.sleep(10)
            await self.refresh_rpcs()

    async def ping_rpc(self, url: str) -> float:
        try:
            w3 = AsyncWeb3(AsyncHTTPProvider(url))
            start = time.perf_counter()
            await w3.eth.get_block_number()
            end = time.perf_counter()
            return (end - start) * 1000
        except Exception:
            return float('inf')

    async def refresh_rpcs(self):
        tasks = [self.ping_rpc(url) for url in self.urls]
        results = await asyncio.gather(*tasks)
        
        for url, latency in zip(self.urls, results):
            self.latencies[url] = latency

        healthy_rpcs = {k: v for k, v in self.latencies.items() if v < float('inf')}
        if healthy_rpcs:
            self.active_rpc = min(healthy_rpcs, key=healthy_rpcs.get)
        else:
            logger.error("🚨 CRITICAL: All RPCs are down!")
            
    def get_web3(self) -> AsyncWeb3:
        if not self.active_rpc:
            raise ConnectionError("No healthy RPC available")
        return AsyncWeb3(AsyncHTTPProvider(self.active_rpc))

rpc_manager = RPCManager()
