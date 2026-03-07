from database.db import Database
from models.schemas import UserSettings
from utils.encryption import encrypt_key

class ConfigService:
    @staticmethod
    async def init_user(user_id: int, is_admin: bool):
        await Database.execute("""
            INSERT INTO users (id, is_admin) VALUES ($1, $2) ON CONFLICT (id) DO NOTHING
        """, user_id, is_admin)
        await Database.execute("""
            INSERT INTO settings (user_id) VALUES ($1) ON CONFLICT (user_id) DO NOTHING
        """, user_id)

    @staticmethod
    async def update_setting(user_id: int, field: str, value: any):
        allowed_fields = ['rpc_url', 'copy_percentage', 'max_trade_size', 'risk_limit', 'slippage', 'poll_interval', 'is_active']
        if field in allowed_fields:
            await Database.execute(f"UPDATE settings SET {field} = $1 WHERE user_id = $2", value, user_id)
        elif field == 'private_key':
            enc = encrypt_key(value)
            await Database.execute("UPDATE settings SET encrypted_private_key = $1 WHERE user_id = $2", enc, user_id)

    @staticmethod
    async def get_settings(user_id: int) -> UserSettings:
        row = await Database.fetch("SELECT * FROM settings WHERE user_id = $1", user_id)
        if not row: return None
        r = row[0]
        return UserSettings(
            user_id=r['user_id'], rpc_url=r['rpc_url'], copy_percentage=float(r['copy_percentage']),
            max_trade_size=float(r['max_trade_size']), risk_limit=float(r['risk_limit']),
            slippage=float(r['slippage']), is_active=r['is_active']
        )
