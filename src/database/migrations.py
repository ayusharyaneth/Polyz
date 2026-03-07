# src/database/migrations.py
from src.database.db import db_pool
from src.utils.logger import get_logger

logger = get_logger(__name__)

async def run_migrations():
    logger.info("Running migrations...")
    schema = """
    CREATE TABLE IF NOT EXISTS users (
        id BIGINT PRIMARY KEY,
        private_key TEXT,
        address VARCHAR(42),
        is_active BOOLEAN DEFAULT true
    );
    CREATE TABLE IF NOT EXISTS bot_settings (
        user_id BIGINT PRIMARY KEY REFERENCES users(id),
        copy_percentage NUMERIC DEFAULT 100.0,
        max_trade_size NUMERIC DEFAULT 1000.0,
        max_daily_loss NUMERIC DEFAULT 500.0,
        risk_limit NUMERIC DEFAULT 2000.0,
        rpc_url TEXT
    );
    CREATE TABLE IF NOT EXISTS target_wallets (
        id SERIAL PRIMARY KEY,
        user_id BIGINT REFERENCES users(id),
        address VARCHAR(42),
        label VARCHAR(255),
        UNIQUE(user_id, address)
    );
    CREATE TABLE IF NOT EXISTS positions (
        id SERIAL PRIMARY KEY,
        user_id BIGINT REFERENCES users(id),
        token_id VARCHAR(255),
        amount NUMERIC
    );
    CREATE TABLE IF NOT EXISTS trades (
        id SERIAL PRIMARY KEY,
        user_id BIGINT REFERENCES users(id),
        target_address VARCHAR(42),
        token_id VARCHAR(255),
        side VARCHAR(10),
        size NUMERIC,
        price NUMERIC,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20)
    );
    """
    await db_pool.execute(schema)
    logger.info("Migrations completed.")
