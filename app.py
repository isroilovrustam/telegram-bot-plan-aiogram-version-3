import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from data import config
from handlers import setup_routers
from middlewares import setup_middlewares
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(bot: Bot):
    """Bot ishga tushganda bajariladigan funksiya"""
    # Birlamchi komandalar (/start va /help)
    await set_default_commands(bot)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(bot)

    logging.info("Bot ishga tushdi!")


async def on_shutdown(bot: Bot):
    """Bot to'xtaganda bajariladigan funksiya"""
    logging.info("Bot to'xtatildi!")
    await bot.session.close()


async def main():
    # Logging sozlamalari
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )

    # Bot va Dispatcher yaratish
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Routerlarni sozlash
    setup_routers(dp)

    # Middlewarelarni sozlash
    setup_middlewares(dp)

    # Bot ishga tushganda
    await on_startup(bot)

    try:
        # Polling ni boshlash
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        # Bot to'xtaganda
        await on_shutdown(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi!")