# src/telegram/bot.py
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from src.config.settings import settings
from src.telegram.handlers import (
    start_cmd, ping_cmd, health_cmd, status_cmd, 
    add_wallet_cmd, set_copy_percentage_cmd, 
    set_max_trade_cmd, emergency_sell_cmd, menu_text_handler
)

_app = None

async def start_bot():
    global _app
    _app = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    
    # Register Commands
    _app.add_handler(CommandHandler("start", start_cmd))
    _app.add_handler(CommandHandler("ping", ping_cmd))
    _app.add_handler(CommandHandler("health", health_cmd))
    _app.add_handler(CommandHandler("status", status_cmd))
    _app.add_handler(CommandHandler("add_wallet", add_wallet_cmd))
    _app.add_handler(CommandHandler("set_copy_percentage", set_copy_percentage_cmd))
    _app.add_handler(CommandHandler("set_max_trade", set_max_trade_cmd))
    _app.add_handler(CommandHandler("emergency_sell", emergency_sell_cmd))
    
    # NEW: Catch all regular text messages (which is what the Reply Keyboard sends)
    _app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_text_handler))
    
    await _app.initialize()
    await _app.start()
    await _app.updater.start_polling()

async def send_alert(chat_id: int, text: str):
    if _app and _app.bot:
        try:
            await _app.bot.send_message(chat_id=chat_id, text=text)
        except Exception:
            pass
