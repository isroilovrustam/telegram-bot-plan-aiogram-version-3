from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from filters.is_group import IsGroup
router = Router(name="start")


@router.message(IsGroup(), CommandStart())
async def bot_start(message: Message):
    """
    /start buyrug'i uchun handler
    """
    await message.answer(f"Group, {message.from_user.full_name}!")
