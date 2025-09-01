# bot/app/main.py
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.app.core.config import settings
from bot.app.handlers.admin_handlers import admin_router
from bot.app.handlers.user_handlers import user_router

async def main():
    """
    Main function to configure and start the bot.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    # Bot and Dispatcher setup
    bot = Bot(token=settings.BOT_TOKEN)

    # For now, we'll use in-memory storage. We can switch to Redis later if needed for FSM.
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)

    # Include our command routers
    dp.include_router(user_router)
    dp.include_router(admin_router)

    # Start polling
    try:
        logging.info("Starting bot polling...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")