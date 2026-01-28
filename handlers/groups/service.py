from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.enums import ContentType

from filters.is_group import IsGroup

router = Router(name="members")


@router.message(IsGroup(), F.content_type == ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: Message):
    """Yangi a'zo qo'shilganda"""
    members = ", ".join([m.mention_html() for m in message.new_chat_members])
    await message.reply(f"Xush kelibsiz, {members}.")


@router.message(IsGroup(), F.content_type == ContentType.LEFT_CHAT_MEMBER)
async def left_member(message: Message, bot: Bot):
    """A'zo ketganda yoki haydalganda"""
    left_user = message.left_chat_member

    # O'zi chiqib ketgan bo'lsa
    if left_user.id == message.from_user.id:
        await message.answer(
            f"{left_user.mention_html()} guruhni tark etdi"
        )

    # Bot o'zi haydagan bo'lsa - javob bermaymiz
    elif message.from_user.id == bot.id:
        return

    # Admin haydagan bo'lsa
    else:
        await message.answer(
            f"{left_user.full_name} guruhdan haydaldi. "
            f"Admin: {message.from_user.mention_html()}"
        )