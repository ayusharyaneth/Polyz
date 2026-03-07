# scripts/start_bot.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from main import main

if __name__ == "__main__":
    asyncio.run(main())
