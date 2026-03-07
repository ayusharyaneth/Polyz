CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS settings (
    user_id BIGINT PRIMARY KEY REFERENCES users(id),
    rpc_url TEXT,
    encrypted_private_key TEXT,
    copy_percentage NUMERIC DEFAULT 100.0,
    max_trade_size NUMERIC DEFAULT 1000.0,
    risk_limit NUMERIC DEFAULT 5000.0,
    slippage NUMERIC DEFAULT 1.0,
    poll_interval INTEGER DEFAULT 5,
    is_active BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tracked_wallets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    address VARCHAR(42) UNIQUE NOT NULL,
    label VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS trades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trader_address VARCHAR(42) REFERENCES tracked_wallets(address),
    market_id TEXT NOT NULL,
    direction VARCHAR(10) NOT NULL,
    trader_size NUMERIC NOT NULL,
    copied_size NUMERIC,
    status VARCHAR(20) DEFAULT 'pending',
    tx_hash TEXT,
    error_msg TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS positions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    market_id TEXT NOT NULL,
    size NUMERIC NOT NULL,
    avg_entry_price NUMERIC NOT NULL,
    status VARCHAR(20) DEFAULT 'open',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
