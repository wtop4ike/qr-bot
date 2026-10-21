import asyncio

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import router

async def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit("Set the environment variables BOT_TOKEN and DEFAULT_LANGUAGE before running.")
    async with Bot(BOT_TOKEN) as bot:
        dispatcher = Dispatcher()
        dispatcher.include_router(router)
        await dispatcher.start_polling(bot, allowed_updates=["message"])


if __name__ == "__main__":
    asyncio.run(main())