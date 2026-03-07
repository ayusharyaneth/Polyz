# src/telegram/handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from src.database.db import db_pool
from src.services.health_service import HealthMonitor
from src.telegram.keyboards import main_menu_keyboard

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await db_pool.execute("INSERT INTO users (id) VALUES ($1) ON CONFLICT DO NOTHING", user_id)
    await db_pool.execute("INSERT INTO bot_settings (user_id) VALUES ($1) ON CONFLICT DO NOTHING", user_id)
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

# Add remaining commands mapping similarly (set_copy_percentage, add_wallet, etc.)
# Handlers connect to controllers which update DB.
