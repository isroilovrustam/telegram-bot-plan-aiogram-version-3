from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_subscription_keyboard(channels: list) -> InlineKeyboardMarkup:
    """
    Obuna bo'lish uchun kanallar tugmalarini yaratish

    :param channels: Kanallar ro'yxati [(title, invite_link), ...]
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()

    for title, invite_link in channels:
        builder.row(
            InlineKeyboardButton(text=f"📢 {title}", url=invite_link)
        )

    # Tekshirish tugmasi
    builder.row(
        InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_subs")
    )

    return builder.as_markup()
