# src/telegram/bot.py
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from src.config.settings import settings
from src.telegram.handlers import start_cmd, ping_cmd, health_cmd

_app = None

async def start_bot():
    global _app
    _app = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    
    _app.add_handler(CommandHandler("start", start_cmd))
    _app.add_handler(CommandHandler("ping", ping_cmd))
    _app.add_handler(CommandHandler("health", health_cmd))
    
    await _app.initialize()
    await _app.start()
    await _app.updater.start_polling()

async def send_alert(chat_id: int, text: str):
    if _app and _app.bot:
        try:
            await _app.bot.send_message(chat_id=chat_id, text=text)
        except Exception:
            pass
