import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from telegram.bot import main
from utils.logger import logger

if __name__ == "__main__":
    logger.info("Starting Telegram Bot...")
    main()
