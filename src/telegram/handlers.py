# src/telegram/handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from src.database.db import db_instance
from src.services.health_service import HealthMonitor
from src.telegram.keyboards import main_menu_keyboard

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = db_instance.db
    
    # Upsert user and settings
    await db.users.update_one(
        {"_id": user_id}, 
        {"$setOnInsert": {"_id": user_id, "private_key": None, "address": None, "is_active": True}}, 
        upsert=True
    )
    await db.bot_settings.update_one(
        {"user_id": user_id},
        {"$setOnInsert": {"user_id": user_id, "copy_percentage": 100.0, "max_trade_size": 1000.0, "max_daily_loss": 500.0, "risk_limit": 2000.0, "rpc_url": None}},
        upsert=True
    )
    await update.message.reply_text("👋 Welcome to Polymarket Copy Trading Bot!", reply_markup=main_menu_keyboard())

async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("📡 Measuring latency...")
    stats = await HealthMonitor.ping_all()
    
    text = "📡 *SYSTEM LATENCY*\n\n"
    for k, v in stats.items():
        text += f"{k}: {v}\n"
    
    status = "Healthy ✅" if all("ms" in v for v in stats.values()) else "Degraded ⚠️"
    text += f"\nStatus: {status}"
    
    await msg.edit_text(text, parse_mode="Markdown")

async def health_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ping_cmd(update, context)
