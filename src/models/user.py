# src/models/user.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    private_key: Optional[str]
    address: Optional[str]
    is_active: bool
