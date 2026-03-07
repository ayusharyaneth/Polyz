# src/telegram/keyboards.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📊 Status", callback_data='status'), InlineKeyboardButton("📡 Ping", callback_data='ping')],
        [InlineKeyboardButton("⚙️ Settings", callback_data='settings'), InlineKeyboardButton("🛑 Stop Copying", callback_data='stop')],
        [InlineKeyboardButton("🆘 Emergency Sell", callback_data='emergency_sell')]
    ]
    return InlineKeyboardMarkup(keyboard)
