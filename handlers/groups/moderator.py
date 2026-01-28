import asyncio
import datetime
import re

from aiogram import Router, Bot, F
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from filters import IsGroup, IsAdminFilter

router = Router(name="moderation")


# /ro yoki !ro (read-only) komandalari uchun handler
@router.message(IsGroup(), Command("ro", prefix="!/"), IsAdminFilter())
async def read_only_mode(message: Message, bot: Bot):
    """Foydalanuvchini read-only rejimiga o'tkazish"""

    if not message.reply_to_message:
        await message.answer("❗ Foydalanuvchi xabariga reply qiling!")
        return

    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id

    # Komandani parse qilish
    command_parse = re.compile(r"(!ro|/ro) ?(\d+)? ?([\w+\D]+)?")
    parsed = command_parse.match(message.text)
    time = parsed.group(2)
    comment = parsed.group(3)

    if not time:
        time = 5

    time = int(time)

    # Ban vaqtini hisoblaymiz (hozirgi vaqt + n minut)
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)

    # Ruxsatlarni cheklash
    permissions = ChatPermissions(can_send_messages=False)

    try:
        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=member_id,
            permissions=permissions,
            until_date=until_date
        )
        await message.reply_to_message.delete()
    except TelegramBadRequest as err:
        await message.answer(f"❌ Xatolik! {err.message}")
        return

    # Chatga yozamiz
    await message.answer("""
🔇 Foydalanuvchi {member.full_name} {time} minut yozish huquqidan mahrum qilindi.\n
Sabab: <b>{comment or "ko'rsatilmagan"}</b>"""
    )

    service_message = await message.reply("🕐 Xabar 5 sekunddan so'ng o'chib ketadi.")

    # 5 sekund kutib xabarlarni o'chirib tashlaymiz
    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()


# read-only holatdan qayta tiklaymiz
@router.message(IsGroup(), Command("unro", prefix="!/"), IsAdminFilter())
async def undo_read_only_mode(message: Message, bot: Bot):
    """Foydalanuvchini read-only rejimidan chiqarish"""

    if not message.reply_to_message:
        await message.answer("❗ Foydalanuvchi xabariga reply qiling!")
        return

    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id

    # To'liq ruxsatlarni qaytarish
    user_allowed = ChatPermissions(
        can_send_messages=True,
        can_send_audios=True,
        can_send_documents=True,
        can_send_photos=True,
        can_send_videos=True,
        can_send_video_notes=True,
        can_send_voice_notes=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_invite_users=True,
        can_change_info=False,
        can_pin_messages=False,
    )

    service_message = await message.reply("🕐 Xabar 5 sekunddan so'ng o'chib ketadi.")

    await asyncio.sleep(5)

    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=member_id,
        permissions=user_allowed
    )

    await message.reply(f"✅ Foydalanuvchi {member.full_name} tiklandi")

    # Xabarlarni o'chiramiz
    await message.delete()
    await service_message.delete()


# Foydalanuvchini banga yuborish (guruhdan haydash)
@router.message(IsGroup(), Command("ban", prefix="!/"), IsAdminFilter())
async def ban_user(message: Message, bot: Bot):
    """Foydalanuvchini guruhdan haydash"""

    if not message.reply_to_message:
        await message.answer("❗ Foydalanuvchi xabariga reply qiling!")
        return

    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id

    try:
        await bot.ban_chat_member(chat_id=chat_id, user_id=member_id)
    except TelegramBadRequest as err:
        await message.answer(f"❌ Xatolik! {err.message}")
        return

    await message.answer(
        f"🚫 Foydalanuvchi {member.full_name} guruhdan haydaldi"
    )

    service_message = await message.reply("🕐 Xabar 5 sekunddan so'ng o'chib ketadi.")

    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()


# Foydalanuvchini bandan chiqarish
@router.message(IsGroup(), Command("unban", prefix="!/"), IsAdminFilter())
async def unban_user(message: Message, bot: Bot):
    """Foydalanuvchini bandan chiqarish"""

    if not message.reply_to_message:
        await message.answer("❗ Foydalanuvchi xabariga reply qiling!")
        return

    member = message.reply_to_message.from_user
    member_id = member.id
    chat_id = message.chat.id

    try:
        await bot.unban_chat_member(chat_id=chat_id, user_id=member_id)
    except TelegramBadRequest as err:
        await message.answer(f"❌ Xatolik! {err.message}")
        return

    await message.answer(
        f"✅ Foydalanuvchi {member.full_name} bandan chiqarildi"
    )

    service_message = await message.reply("🕐 Xabar 5 sekunddan so'ng o'chib ketadi.")

    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()
