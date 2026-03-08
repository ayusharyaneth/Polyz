# src/telegram/keyboards.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📉 Positions", callback_data="positions"),
            InlineKeyboardButton("🔔 Track", callback_data="track")
        ],
        [
            InlineKeyboardButton("📊 Markets", callback_data="markets"),
            InlineKeyboardButton("💰 Copy-Trade", callback_data="copy_trade")
        ],
        [
            InlineKeyboardButton("💳 Wallets", callback_data="wallets"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings")
        ],
        [
            InlineKeyboardButton("📋 Limit Orders", callback_data="limit_orders"),
            InlineKeyboardButton("⚡️ Health", callback_data="health") # Replaced Close with Health
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
