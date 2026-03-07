# src/models/settings.py
from dataclasses import dataclass

@dataclass
class BotSettings:
    user_id: int
    copy_percentage: float
    max_trade_size: float
    max_daily_loss: float
    risk_limit: float
    rpc_url: str
