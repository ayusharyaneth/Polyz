# src/models/wallet.py
from dataclasses import dataclass

@dataclass
class TargetWallet:
    id: int
    user_id: int
    address: str
    label: str
