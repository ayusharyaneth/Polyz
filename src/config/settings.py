# src/config/settings.py
import os
from dotenv import load_dotenv

# override=True ensures your .env file always wins over cached shell variables
load_dotenv(override=True)

class Settings:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ERROR_DUMP_CHAT_ID = os.getenv("ERROR_DUMP_CHAT_ID")
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    POLYMARKET_HOST = os.getenv("POLYMARKET_HOST", "https://clob.polymarket.com")
    CHAIN_ID = int(os.getenv("CHAIN_ID", 137))
    
    # If POLYGON_RPC_URL is set in .env, use it. Otherwise, fallback to public nodes.
    _custom_rpc = os.getenv("POLYGON_RPC_URL")
    DEFAULT_RPC_URLS = [_custom_rpc] if _custom_rpc else [
        "https://polygon-rpc.com",
        "https://rpc.ankr.com/polygon",
        "https://polygon.llamarpc.com"
    ]
    
    CTF_CONTRACT = "0x4d97dcd97ec945f40cf65f87097ace5ea0476045"
    
settings = Settings()
