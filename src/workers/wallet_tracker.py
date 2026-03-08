# src/workers/wallet_tracker.py
import asyncio
import json
from src.services.rpc_manager import rpc_manager
from src.config.settings import settings
from src.utils.logger import get_logger
from src.database.db import db_instance
import redis.asyncio as redis

logger = get_logger(__name__)

class WalletTracker:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)

    async def start(self):
        logger.info("Wallet tracker started")
        
        w3 = rpc_manager.get_web3()
        abi = [{"anonymous":False,"inputs":[{"indexed":True,"name":"operator","type":"address"},{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"id","type":"uint256"},{"indexed":False,"name":"value","type":"uint256"}],"name":"TransferSingle","type":"event"}]
        contract = w3.eth.contract(address=w3.to_checksum_address(settings.CTF_CONTRACT), abi=abi)
        
        # Start tracking from a few blocks in the past to ensure node stability
        try:
            last_checked_block = await w3.eth.get_block_number() - 5
        except Exception:
            last_checked_block = 0 # Will update on first successful loop
        
        while True:
            try:
                wallets = await db_instance.db.target_wallets.find({}, {"address": 1}).to_list(None)
                target_addresses = [w3.to_checksum_address(w['address']) for w in wallets if 'address' in w]

                if not target_addresses:
                    await asyncio.sleep(10)
                    continue

                latest_block = await w3.eth.get_block_number()
                safe_latest_block = latest_block - 2 # Stay 2 blocks behind to prevent -32000 errors

                # If we've already checked this block, wait for the next one
                if last_checked_block >= safe_latest_block:
                    await asyncio.sleep(2)
                    continue

                # Fetch logs safely between the last check and the current safe block
                events = await contract.events.TransferSingle.get_logs(
                    from_block=last_checked_block + 1, 
                    to_block=safe_latest_block
                )
                
                for event in events:
                    args = event['args']
                    from_addr = args['from']
                    to_addr = args['to']
                    
                    if to_addr in target_addresses:
                        await self.publish_trade(to_addr, str(args['id']), args['value'], True)
                    elif from_addr in target_addresses:
                        await self.publish_trade(from_addr, str(args['id']), args['value'], False)
                
                # Update our memory
                last_checked_block = safe_latest_block
                await asyncio.sleep(3)
                
            except Exception as e:
                # Mute the specific -32000 error if it somehow slips through during a node reboot
                if "-32000" not in str(e):
                    logger.error("Wallet tracker error", error=str(e))
                
                # Gently grab a fresh connection and try again
                await asyncio.sleep(5)
                w3 = rpc_manager.get_web3()
                contract = w3.eth.contract(address=w3.to_checksum_address(settings.CTF_CONTRACT), abi=abi)

    async def publish_trade(self, address: str, token_id: str, amount: int, is_buy: bool):
        payload = {"address": address, "token_id": token_id, "amount": amount, "is_buy": is_buy}
        await self.redis.publish("new_trades", json.dumps(payload))
