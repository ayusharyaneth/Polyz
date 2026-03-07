# scripts/start_worker.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from src.workers.trade_listener import TradeListener
from src.workers.wallet_tracker import WalletTracker

async def run():
    tracker = WalletTracker()
    listener = TradeListener()
    await asyncio.gather(tracker.start(), listener.start())

if __name__ == "__main__":
    asyncio.run(run())
