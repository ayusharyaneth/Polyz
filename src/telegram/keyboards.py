# src/telegram/keyboards.py
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("📈 Positions"), KeyboardButton("🔔 Track")],
        [KeyboardButton("📊 Markets"), KeyboardButton("💰 Copy-Trade")],
        [KeyboardButton("💳 Wallets"), KeyboardButton("⚙️ Settings")],
        [KeyboardButton("📋 Limit Orders"), KeyboardButton("⚡️ Health")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, is_persistent=True)

def positions_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➤ 🟢 Open (0)", callback_data="pos_open"),
            InlineKeyboardButton("🔴 Closed (0)", callback_data="pos_closed"),
            InlineKeyboardButton("💰 Redeem (0)", callback_data="pos_redeem")
        ],
        [InlineKeyboardButton("⚙️ Min Value: $0.00", callback_data="pos_min_val")],
        [
            InlineKeyboardButton("💳 W1", callback_data="pos_w1"),
            InlineKeyboardButton("🔄 Refresh", callback_data="pos_refresh")
        ],
        [
            InlineKeyboardButton("← Home", callback_data="home"),
            InlineKeyboardButton("× Close", callback_data="close")
        ]
    ])

def track_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Add Wallet", callback_data="track_add"),
            InlineKeyboardButton("Mass Import", callback_data="track_import")
        ],
        [
            InlineKeyboardButton("← Back", callback_data="back"),
            InlineKeyboardButton("× Close", callback_data="close")
        ]
    ])

def copy_trade_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Add Task", callback_data="copy_add"),
            InlineKeyboardButton("Remove Task", callback_data="copy_remove")
        ],
        [
            InlineKeyboardButton("← Back", callback_data="back"),
            InlineKeyboardButton("× Close", callback_data="close")
        ]
    ])

def wallets_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔑 Generate Wallet", callback_data="wallet_gen"),
            InlineKeyboardButton("🔄 Refresh", callback_data="wallet_refresh")
        ],
        [InlineKeyboardButton("💳 Deposit Fiat", callback_data="wallet_fiat")],
        [
            InlineKeyboardButton("💸 Withdraw", callback_data="wallet_withdraw"),
            InlineKeyboardButton("📥 Deposit", callback_data="wallet_deposit")
        ],
        [
            InlineKeyboardButton("⭐ Set Default", callback_data="wallet_default"),
            InlineKeyboardButton("📊 Portfolio", callback_data="wallet_portfolio")
        ],
        [
            InlineKeyboardButton("📦 Archive Wallet", callback_data="wallet_archive"),
            InlineKeyboardButton("📂 Unarchive Wallet", callback_data="wallet_unarchive")
        ],
        [InlineKeyboardButton("👤 Profile", callback_data="wallet_profile")],
        [
            InlineKeyboardButton("← Back", callback_data="back"),
            InlineKeyboardButton("× Close", callback_data="close")
        ]
    ])

def limit_orders_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💳 Switch Wallet", callback_data="limit_switch"),
            InlineKeyboardButton("🔄 Refresh", callback_data="limit_refresh")
        ],
        [
            InlineKeyboardButton("← Back", callback_data="back"),
            InlineKeyboardButton("× Close", callback_data="close")
        ]
    ])

def settings_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💰 Buy Presets", callback_data="set_buy"),
            InlineKeyboardButton("💰 Sell Presets", callback_data="set_sell")
        ],
        [
            InlineKeyboardButton("📉 Stop Loss", callback_data="set_stoploss"),
            InlineKeyboardButton("🔐 Two-Factor Auth", callback_data="set_2fa")
        ],
        [InlineKeyboardButton("📊 Slippage: Default (5%)", callback_data="set_slippage")],
        [InlineKeyboardButton("Auto Redeem: ON", callback_data="set_autoredeem")],
        [InlineKeyboardButton("Auto-Claim Alerts: ON", callback_data="set_autoclaim")],
        [
            InlineKeyboardButton("← Back", callback_data="back"),
            InlineKeyboardButton("× Close", callback_data="close")
        ]
    ])
