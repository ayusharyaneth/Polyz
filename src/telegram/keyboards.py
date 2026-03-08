# src/telegram/keyboards.py
from telegram import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    # 2-column grid exactly like your screenshot, but swapping Close for Health
    keyboard = [
        [KeyboardButton("📈 Positions"), KeyboardButton("🔔 Track")],
        [KeyboardButton("📊 Markets"), KeyboardButton("💰 Copy-Trade")],
        [KeyboardButton("💳 Wallets"), KeyboardButton("⚙️ Settings")],
        [KeyboardButton("📋 Limit Orders"), KeyboardButton("⚡️ Health")]
    ]
    # resize_keyboard=True makes it perfectly hug the bottom of the phone screen
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)
