import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_ADMIN_ID = int(os.getenv("BOT_ADMIN_ID", 0))
ALERT_CHANNEL_ID = os.getenv("ALERT_CHANNEL_ID")
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "").encode()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

RPC_LATENCY_THRESHOLD_MS = 2000
DB_LATENCY_THRESHOLD_MS = 500
REDIS_LATENCY_THRESHOLD_MS = 300
