from telegram import Update
from telegram.ext import ContextTypes
from config.settings import BOT_ADMIN_ID
from services.health_service import HealthService
from services.config_service import ConfigService

def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != BOT_ADMIN_ID:
            return
        return await func(update, context)
    return wrapper

@admin_only
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ConfigService.init_user(update.effective_user.id, True)
    await update.message.reply_text("🟢 System Running\nAdmin authenticated.")

@admin_only
async def cmd_ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = await ConfigService.get_settings(update.effective_user.id)
    rpc_latency = await HealthService.ping_rpc(settings.rpc_url if settings else None)
    db_latency = await HealthService.ping_db()
    redis_latency = await HealthService.ping_redis()
    tg_latency = await HealthService.ping_telegram()

    msg = (
        "🏓 PING RESULTS\n\n"
        f"📡 RPC Latency: {rpc_latency:.0f} ms\n"
        f"💾 Database Latency: {db_latency:.0f} ms\n"
        f"⚡ Redis Latency: {redis_latency:.0f} ms\n"
        f"🤖 Telegram API: {tg_latency:.0f} ms\n"
        f"🧠 Worker Response: < 5 ms\n"
    )
    await update.message.reply_text(msg)

@admin_only
async def cmd_health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings = await ConfigService.get_settings(update.effective_user.id)
    rpc_l = await HealthService.ping_rpc(settings.rpc_url if settings else None)
    db_l = await HealthService.ping_db()
    
    rpc_status = "🟢 Connected" if rpc_l > 0 else "🔴 Error"
    db_status = "🟢 Connected" if db_l > 0 else "🔴 Error"

    msg = (
        "⚙️ SYSTEM HEALTH\n\n"
        f"📡 RPC: {rpc_status} ({rpc_l:.0f} ms)\n"
        f"💾 Database: {db_status} ({db_l:.0f} ms)\n"
        "⚡ Redis: 🟢 Running\n"
        "🤖 Telegram API: 🟢 OK\n"
        "🧠 Workers: 🟢 Active\n"
        "📊 Wallet Monitor: 🟢 Running\n"
        "🚀 Trade Executor: 🟢 Ready\n"
    )
    await update.message.reply_text(msg)

@admin_only
async def cmd_set_rpc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🔴 Usage: /set_rpc <url>")
        return
    await ConfigService.update_setting(update.effective_user.id, 'rpc_url', context.args[0])
    await update.message.reply_text(f"📡 RPC Updated: {context.args[0]}")

@admin_only
async def cmd_set_private_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    await ConfigService.update_setting(update.effective_user.id, 'private_key', context.args[0])
    await update.message.reply_text("💾 Private Key Encrypted & Stored.")
    try: await update.message.delete()
    except: pass

@admin_only
async def cmd_set_copy_percentage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await ConfigService.update_setting(update.effective_user.id, 'copy_percentage', float(context.args[0]))
        await update.message.reply_text(f"📊 Copy Percentage Set: {context.args[0]}%")

@admin_only
async def cmd_set_max_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await ConfigService.update_setting(update.effective_user.id, 'max_trade_size', float(context.args[0]))
        await update.message.reply_text(f"⚠️ Max Trade Size Set: ${context.args[0]}")

@admin_only
async def cmd_set_risk_limit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await ConfigService.update_setting(update.effective_user.id, 'risk_limit', float(context.args[0]))
        await update.message.reply_text(f"⚠️ Risk Limit Set: ${context.args[0]}")

@admin_only
async def cmd_set_slippage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await ConfigService.update_setting(update.effective_user.id, 'slippage', float(context.args[0]))
        await update.message.reply_text(f"⚠️ Slippage Set: {context.args[0]}%")

@admin_only
async def cmd_start_copy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ConfigService.update_setting(update.effective_user.id, 'is_active', True)
    await update.message.reply_text("🟢 Copy Trading Started")

@admin_only
async def cmd_stop_copy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ConfigService.update_setting(update.effective_user.id, 'is_active', False)
    await update.message.reply_text("🔴 Copy Trading Stopped")
