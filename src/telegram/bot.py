from telegram.ext import ApplicationBuilder, CommandHandler
from config.settings import TELEGRAM_BOT_TOKEN
from telegram.handlers import (
    cmd_start, cmd_ping, cmd_health, cmd_set_rpc, cmd_set_private_key, 
    cmd_set_copy_percentage, cmd_set_max_trade, cmd_set_risk_limit, 
    cmd_set_slippage, cmd_start_copy, cmd_stop_copy
)
from database.db import Database

async def post_init(application):
    await Database.connect()

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("ping", cmd_ping))
    app.add_handler(CommandHandler("health", cmd_health))
    app.add_handler(CommandHandler("set_rpc", cmd_set_rpc))
    app.add_handler(CommandHandler("set_private_key", cmd_set_private_key))
    app.add_handler(CommandHandler("set_copy_percentage", cmd_set_copy_percentage))
    app.add_handler(CommandHandler("set_max_trade", cmd_set_max_trade))
    app.add_handler(CommandHandler("set_risk_limit", cmd_set_risk_limit))
    app.add_handler(CommandHandler("set_slippage", cmd_set_slippage))
    app.add_handler(CommandHandler("start_copy", cmd_start_copy))
    app.add_handler(CommandHandler("stop_copy", cmd_stop_copy))

    app.run_polling()
