# src/telegram/handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from src.database.db import db_instance
from src.services.health_service import HealthMonitor
from src.telegram.keyboards import main_menu_keyboard

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = db_instance.db
    
    await db.users.update_one(
        {"_id": user_id}, 
        {"$setOnInsert": {"_id": user_id, "private_key": None, "address": None, "is_active": True}}, 
        upsert=True
    )
    await db.bot_settings.update_one(
        {"user_id": user_id},
        {"$setOnInsert": {"user_id": user_id, "copy_percentage": 100.0, "max_trade_size": 1000.0, "max_daily_loss": 500.0}},
        upsert=True
    )
    await update.message.reply_text("👋 Welcome to Polymarket Copy Trading Bot!", reply_markup=main_menu_keyboard())

async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Safely handle both typed commands and button clicks
    message = update.message or update.callback_query.message
    msg = await message.reply_text("📡 Measuring latency...")
    stats = await HealthMonitor.ping_all()
    
    text = "📡 *SYSTEM LATENCY*\n\n"
    for k, v in stats.items():
        text += f"{k}: {v}\n"
    
    status = "Healthy ✅" if all("ms" in str(v) for v in stats.values()) else "Degraded ⚠️"
    text += f"\nStatus: {status}"
    
    await msg.edit_text(text, parse_mode="Markdown")
async def health_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = db_instance.db
    
    # Fetch configurations from MongoDB
    user = await db.users.find_one({"_id": user_id})
    settings = await db.bot_settings.find_one({"user_id": user_id})
    wallet_count = await db.target_wallets.count_documents({"user_id": user_id})
    
    # Minimal Status Flags
    pk_status = "✅ Active" if user and user.get("private_key") else "❌ Missing"
    rpc_status = "✅ Custom" if settings and settings.get("rpc_url") else "⚠️ Public"
    wallet_status = f"✅ {wallet_count}" if wallet_count > 0 else "❌ 0"
    
    pct = settings.get('copy_percentage', 100) if settings else 100
    max_t = settings.get('max_trade_size', 1000) if settings else 1000
    max_l = settings.get('max_daily_loss', 500) if settings else 500

    # Sleek Terminal-Style Dashboard
    text = (
        "⚡️ *System Health*\n\n"
        "*Core*\n"
        f"├ 🔑 Auth: {pk_status}\n"
        f"├ 🌐 RPC: {rpc_status}\n"
        f"└ 🎯 Wallets: {wallet_status}\n\n"
        "*Limits*\n"
        f"├ ⚖️ Copy: {pct}%\n"
        f"├ 💰 Max Trade: ${max_t}\n"
        f"└ 🛡️ Daily Loss: ${max_l}"
    )
    
    message = update.message or update.callback_query.message
    await message.reply_text(text, parse_mode="Markdown")
