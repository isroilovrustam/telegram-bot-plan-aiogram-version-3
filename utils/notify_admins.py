import logging

from aiogram import Bot

from data.config import ADMINS


async def on_startup_notify(bot: Bot):
    """
    Bot ishga tushganda adminlarga xabar yuborish
    """
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=admin, text="✅ Bot ishga tushdi!")
        except Exception as err:
            logging.exception(f"Admin {admin} ga xabar yuborishda xatolik: {err}")
