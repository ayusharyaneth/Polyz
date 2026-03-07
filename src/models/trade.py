# src/models/trade.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    id: int
    user_id: int
    target_address: str
    token_id: str
    side: str
    size: float
    price: float
    timestamp: datetime
    status: str
