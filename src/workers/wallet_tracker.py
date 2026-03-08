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
        
        while True:
            try:
                wallets = await db_instance.db.target_wallets.find({}, {"address": 1}).to_list(None)
                target_addresses = [w3.to_checksum_address(w['address']) for w in wallets if 'address' in w]

                if not target_addresses:
                    await asyncio.sleep(10)
                    continue

                latest_block = await w3.eth.get_block_number()
                
                # The node will happily accept this because both are integers
                events = await contract.events.TransferSingle.get_logs(
                    from_block=latest_block - 5, 
                    to_block=latest_block
                )
                
                for event in events:
                    args = event['args']
                    from_addr = args['from']
                    to_addr = args['to']
                    
                    if to_addr in target_addresses:
                        await self.publish_trade(to_addr, str(args['id']), args['value'], True)
                    elif from_addr in target_addresses:
                        await self.publish_trade(from_addr, str(args['id']), args['value'], False)
                        
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error("Wallet tracker error", error=str(e))
                w3 = rpc_manager.get_web3()
                contract = w3.eth.contract(address=w3.to_checksum_address(settings.CTF_CONTRACT), abi=abi)
                await asyncio.sleep(5)

    async def publish_trade(self, address: str, token_id: str, amount: int, is_buy: bool):
        payload = {"address": address, "token_id": token_id, "amount": amount, "is_buy": is_buy}
        await self.redis.publish("new_trades", json.dumps(payload))
