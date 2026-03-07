# src/models/position.py
from dataclasses import dataclass

@dataclass
class Position:
    id: int
    user_id: int
    token_id: str
    amount: float
