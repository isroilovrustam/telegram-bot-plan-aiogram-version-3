from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name="start")


@router.message(CommandStart())
async def bot_start(message: Message):
    """
    /start buyrug'i uchun handler
    """
    await message.answer(f"Salom, {message.from_user.full_name}!")
