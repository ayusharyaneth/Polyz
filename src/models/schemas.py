from dataclasses import dataclass
from typing import Optional

@dataclass
class TradeEvent:
    trader_address: str
    market_id: str
    direction: str
    position_size: float
    trader_balance: float

@dataclass
class UserSettings:
    user_id: int
    rpc_url: Optional[str]
    copy_percentage: float
    max_trade_size: float
    risk_limit: float
    slippage: float
    is_active: bool
