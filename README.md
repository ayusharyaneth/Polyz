# Polyz

A production-ready, highly concurrent asynchronous copy trading bot for Polymarket controlled entirely via Telegram. Built for reliability with RPC failover, health monitoring, EIP-712 native signing, and comprehensive risk management.

---

## 📦 Requirements

- Python 3.11+
- PostgreSQL
- Redis
- Polygon RPC node access

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/ayusharyaneth/polyz.git
cd polyz
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Upgrade pip (Recommended)

```bash
pip install --upgrade pip
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and configure:

### 6. Running Polyz

```bash
python3 main.py
```

### 🔄 Updating

```bash
git pull origin main
pip install -r requirements.txt
```

## ⚠️ Notes

- Ensure Python 3.11+ is installed  
- Always validate strategy parameters before running in production  
- Never expose your `.env` file publicly  

---

## Configuration

#### 1. Generating "ENCRYPTION_KEY"
You must generate a Fernet encryption key to safely store user private keys in the database

```bash
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```
---

## Telegram Commands

### Signal Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot and database records. |
| `/ping` | Check latency across RPC, Web3 API, DB, and Redis. |
| `/health` | Comprehensive system overview. |
| `/status` | Current copy status. |
| `/add_wallet <address> <label>` | Add a trader to follow. |
| `/set_copy_percentage <int>` | Set sizing fraction. |
| `/set_max_trade <float>` | Set max allowed position size. |
| `/emergency_sell` | Dumps all active Polymarket positions. |

---
