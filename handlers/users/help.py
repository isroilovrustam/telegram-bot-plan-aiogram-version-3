from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from filters.is_private import IsPrivate
router = Router(name="help")


@router.message(IsPrivate(), Command("help"))
async def bot_help(message: Message):
    """
    /help buyrug'i uchun handler
    """
    text = (
        "Buyruqlar: ",
        "/start - Botni ishga tushirish",
        "/help - Yordam"
    )
    await message.answer("\n".join(text))
