# src/telegram/handlers.py
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from src.database.db import db_instance
from src.services.health_service import HealthMonitor
from src.telegram.keyboards import (
    main_menu_keyboard, positions_kb, track_kb, copy_trade_kb, 
    wallets_kb, limit_orders_kb, settings_kb
)

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
    
    await update.message.reply_text(
        "Welcome back to Polyz! 🎰\n\nReady to trade? Fund your wallet and start copy trading!", 
        reply_markup=main_menu_keyboard()
    )

async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    user = await db.users.find_one({"_id": user_id})
    settings = await db.bot_settings.find_one({"user_id": user_id})
    wallet_count = await db.target_wallets.count_documents({"user_id": user_id})
    
    pk_status = "✅ Active" if user and user.get("private_key") else "❌ Missing"
    rpc_status = "✅ Custom" if settings and settings.get("rpc_url") else "⚠️ Public"
    wallet_status = f"✅ {wallet_count}" if wallet_count > 0 else "❌ 0"
    
    pct = settings.get('copy_percentage', 100) if settings else 100
    max_t = settings.get('max_trade_size', 1000) if settings else 1000
    max_l = settings.get('max_daily_loss', 500) if settings else 500

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
        await update.message.reply_text("⚠️ Usage: `/set_copy_percentage <number>`", parse_mode="Markdown")
        return
    try:
        pct = float(context.args[0])
        await db_instance.db.bot_settings.update_one({"user_id": update.effective_user.id}, {"$set": {"copy_percentage": pct}})
        await update.message.reply_text(f"✅ Copy percentage set to {pct}%")
    except ValueError:
        await update.message.reply_text("⚠️ Please provide a valid number.")

async def set_max_trade_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: `/set_max_trade <dollar_amount>`", parse_mode="Markdown")
        return
    try:
        amt = float(context.args[0])
        await db_instance.db.bot_settings.update_one({"user_id": update.effective_user.id}, {"$set": {"max_trade_size": amt}})
        await update.message.reply_text(f"✅ Max trade size set to ${amt}")
    except ValueError:
        await update.message.reply_text("⚠️ Please provide a valid number.")

async def emergency_sell_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚨 *EMERGENCY SELL TRIGGERED*\n\nClosing all active positions at market price...", parse_mode="Markdown")

# Catches clicks on the new inline buttons
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 
    
    if query.data == 'close':
        await query.message.delete()
    else:
        await query.message.reply_text(f"Button `{query.data}` clicked (Action pending execution logic)", parse_mode="Markdown")

# Catches text input from the bottom dashboard
async def menu_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    now = datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]
    user_id = update.effective_user.id
    
    if text == "📈 Positions":
        msg = (
            "📈 **Open Positions**\n\n"
            "*No positions found.*\n\n"
            "💡 *Start trading to see your positions — use tabs to switch views.*\n"
            f"🕒 Last updated: {now}"
        )
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=positions_kb())
        
    elif text == "🔔 Track":
        db = db_instance.db
        wallets = await db.target_wallets.find({"user_id": user_id}).to_list(None)
        
        msg = (
            "⚡️ **Wallet Tracker**\n\n"
            "*Track the bets of any wallet on Polymarket.*\n\n"
            f"📋 **Tracked Wallets ({len(wallets)})**\n\n"
        )
        
        if wallets:
            for i, w in enumerate(wallets, 1):
                msg += f"{i}. 🔔 **{w.get('label', 'Wallet')}**\n`{w['address']}`\n🔕 Mute · 🗑️ Remove\n\n"
        
        msg += "💡 *Select \"Add Wallet\" to track a new wallet.*"
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=track_kb())
        
    elif text == "📊 Markets":
        msg = "📊 *Markets*\n\nLive API sync pending..."
        await update.message.reply_text(msg, parse_mode="Markdown")
        
    elif text == "💰 Copy-Trade":
        msg = (
            "⚡️ **Copy Trade**\n\n"
            "*Automatically copy trades from any wallet on Polymarket.*\n\n"
            "💡 **Your Tasks (0/50)**\n\n"
            "*No tasks yet. Add a task to start copy trading.*\n\n"
            "⚡️ **Status:** No active tasks."
        )
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=copy_trade_kb())
        
    elif text == "💳 Wallets":
        msg = (
            "⚡️ **Wallet Manager**\n\n"
            "*Manage your wallets directly through the bot wallet manager.*\n\n"
            "💳 **Your Wallets (1)**\n\n"
            "1. W1: 0.00 USDC.e ⭐\n`0x0000000000000000000000000000000000000000`\n\n"
            "⚠️ *Do not send funds directly to the wallet address above. Use the \"Deposit\" button below to fund your wallet safely.*\n\n"
            "💡 *What would you like to do?*\n"
            f"🕒 Last updated: {now}"
        )
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=wallets_kb())
        
    elif text == "⚙️ Settings":
        msg = (
            "⚡️ **Settings**\n\n"
            "*Customize your trading preferences, presets, and risk management options below.*\n\n"
            "💡 **Select a setting to configure:**"
        )
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=settings_kb())
        
    elif text == "📋 Limit Orders":
        msg = (
            "📋 **Active Limit Orders**\n\n"
            "💳 Wallet: W1\n\n"
            "📬 *No active limit orders*"
        )
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=limit_orders_kb())
        
    elif text == "⚡️ Health":
        await health_cmd(update, context)
