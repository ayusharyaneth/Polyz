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

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = await db_instance.db.bot_settings.find_one({"user_id": user_id})
    wallets = await db_instance.db.target_wallets.find({"user_id": user_id}).to_list(None)

    message = update.message or update.callback_query.message

    if not settings:
        await message.reply_text("Please run /start first.")
        return

    text = "📊 *Bot Status*\n\n"
    text += f"Copy Percentage: {settings.get('copy_percentage', 100)}%\n"
    text += f"Max Trade Size: ${settings.get('max_trade_size', 1000)}\n\n"
    text += "*Tracked Wallets:*\n"
    
    if wallets:
        for w in wallets:
            text += f"- `{w['address'][:6]}...{w['address'][-4:]}` ({w.get('label', 'Unlabeled')})\n"
    else:
        text += "None currently tracked."

    await message.reply_text(text, parse_mode="Markdown")

async def add_wallet_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Usage: `/add_wallet <address> <label>`\nExample: `/add_wallet 0x123... Whale`", parse_mode="Markdown")
        return
        
    address = context.args[0]
    label = " ".join(context.args[1:])
    user_id = update.effective_user.id
    
    await db_instance.db.target_wallets.update_one(
        {"user_id": user_id, "address": address},
        {"$set": {"label": label}},
        upsert=True
    )
    await update.message.reply_text(f"✅ Wallet added!\nAddress: `{address}`\nLabel: {label}", parse_mode="Markdown")

async def set_copy_percentage_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: `/set_copy_percentage <number>`\nExample: `/set_copy_percentage 50`", parse_mode="Markdown")
        return
        
    try:
        pct = float(context.args[0])
        await db_instance.db.bot_settings.update_one({"user_id": update.effective_user.id}, {"$set": {"copy_percentage": pct}})
        await update.message.reply_text(f"✅ Copy percentage set to {pct}%")
    except ValueError:
        await update.message.reply_text("⚠️ Please provide a valid number.")

# Handles inline keyboard button clicks
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Stops the loading circle on the button
    
    if query.data == 'status':
        await status_cmd(update, context)
    elif query.data == 'ping':
        await ping_cmd(update, context)
    elif query.data == 'settings':
        await query.message.reply_text("⚙️ *Settings Commands:*\n\n`/set_copy_percentage <amount>`\n`/set_max_trade <amount>`\n`/add_wallet <address> <label>`\n`/health`", parse_mode="Markdown")
    elif query.data == 'stop':
        await query.message.reply_text("🛑 Copy trading stopped. (Feature pending execution link)")
    elif query.data == 'emergency_sell':
        await query.message.reply_text("🆘 Emergency Sell triggered! (Feature pending exchange link)")
