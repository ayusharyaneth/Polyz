# src/services/polymarket_client.py
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
from src.config.settings import settings
from src.utils.helpers import decrypt_key
from src.utils.logger import get_logger
from src.database.db import db_instance

logger = get_logger(__name__)

class PolymarketClient:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.client = None

    async def initialize(self):
        user = await db_instance.db.users.find_one({"_id": self.user_id})
        if not user or not user.get('private_key'):
            raise ValueError("Private key not configured")
            
        pk = decrypt_key(user['private_key'])
        
        self.client = ClobClient(
            host=settings.POLYMARKET_HOST,
            key=pk,
            chain_id=settings.CHAIN_ID
        )
        self.client.set_credentials(self.client.create_or_derive_api_creds())

    async def get_markets(self):
        return self.client.get_markets()

    async def get_orderbook(self, token_id: str):
        return self.client.get_order_book(token_id)

    async def submit_order(self, token_id: str, side: str, price: float, size: float):
        if not self.client:
            await self.initialize()

        order_args = OrderArgs(
            price=price,
            size=size,
            side=side.upper(),
            token_id=token_id
        )
        
        signed_order = self.client.create_order(order_args)
        response = self.client.post_order(signed_order, OrderType.GTC)
        logger.info("Order submitted", response=response)
        return response
