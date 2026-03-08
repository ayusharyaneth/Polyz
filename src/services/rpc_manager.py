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
        self.rpcs = settings.DEFAULT_RPC_URLS
        self.active_rpc = None
        self.latencies = {}
        self._w3 = None

    async def initialize(self):
        await self._update_best_rpc()
        asyncio.create_task(self.monitor_rpcs())

    async def _update_best_rpc(self):
        fastest_rpc = None
        best_ping = float('inf')

        # Safely ping all RPCs using a properly closed session
        async with aiohttp.ClientSession() as session:
            for rpc in self.rpcs:
                start = time.perf_counter()
                try:
                    payload = {"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}
                    async with session.post(rpc, json=payload, timeout=3) as resp:
                        if resp.status == 200:
                            ping = (time.perf_counter() - start) * 1000
                            self.latencies[rpc] = ping
                            if ping < best_ping:
                                best_ping = ping
                                fastest_rpc = rpc
                except Exception:
                    self.latencies[rpc] = float('inf')

        # FIX: ONLY create a new Web3 instance if the fastest RPC actually changed!
        if fastest_rpc and fastest_rpc != self.active_rpc:
            self.active_rpc = fastest_rpc
            self._w3 = AsyncWeb3(AsyncHTTPProvider(self.active_rpc))
            logger.info(f"Switched RPC: {self.active_rpc} ({best_ping:.0f}ms)")
        elif not fastest_rpc and not self.active_rpc:
            logger.error("CRITICAL: All RPCs are down!")

    async def monitor_rpcs(self):
        while True:
            await asyncio.sleep(60) # Check latencies once a minute
            await self._update_best_rpc()

    def get_web3(self):
        if not self._w3:
            self._w3 = AsyncWeb3(AsyncHTTPProvider(self.rpcs[0]))
        return self._w3

rpc_manager = RPCManager()
