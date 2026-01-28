import io
from aiogram import Router, Bot
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command

from filters import IsGroup, IsAdminFilter

router = Router(name="group_settings")


@router.message(IsGroup(), Command("set_photo", prefix="!/"), IsAdminFilter())
async def set_new_photo(message: Message, bot: Bot):
    """Guruh rasmini o'zgartirish"""

    if not message.reply_to_message:
        await message.answer("❗ Rasm bilan xabarga reply qiling!")
        return

    if not message.reply_to_message.photo:
        await message.answer("❗ Bu xabarda rasm yo'q!")
        return

    source_message = message.reply_to_message
    photo = source_message.photo[-1]

    # Rasmni yuklab olish
    photo_file = await bot.download(photo)
    photo_bytes = photo_file.read()

    # InputFile yaratish
    input_file = BufferedInputFile(photo_bytes, filename="photo.jpg")

    # Guruh rasmini o'rnatish
    await bot.set_chat_photo(chat_id=message.chat.id, photo=input_file)
    await message.answer("✅ Guruh rasmi o'zgartirildi!")


@router.message(IsGroup(), Command("set_title", prefix="!/"), IsAdminFilter())
async def set_new_title(message: Message, bot: Bot):
    """Guruh nomini o'zgartirish"""

    if not message.reply_to_message:
        await message.answer("❗ Yangi nom yozilgan xabarga reply qiling!")
        return

    if not message.reply_to_message.text:
        await message.answer("❗ Bu xabarda matn yo'q!")
        return

    title = message.reply_to_message.text

    await bot.set_chat_title(chat_id=message.chat.id, title=title)
    await message.answer(f"✅ Guruh nomi o'zgartirildi: {title}")


@router.message(IsGroup(), Command("set_description", prefix="!/"), IsAdminFilter())
async def set_new_description(message: Message, bot: Bot):
    """Guruh tavsifini o'zgartirish"""

    if not message.reply_to_message:
        await message.answer("❗ Yangi tavsif yozilgan xabarga reply qiling!")
        return

    if not message.reply_to_message.text:
        await message.answer("❗ Bu xabarda matn yo'q!")
        return

    description = message.reply_to_message.text

    await bot.set_chat_description(chat_id=message.chat.id, description=description)
    await message.answer("✅ Guruh tavsifi o'zgartirildi!")
