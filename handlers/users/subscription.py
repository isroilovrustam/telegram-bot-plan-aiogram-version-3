from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from data.config import CHANNELS
from utils.misc import subscription
from keyboards.inline.subscription import get_subscription_keyboard

router = Router(name="subscription")


@router.callback_query(F.data == "check_subs")
async def check_subscription(callback: CallbackQuery, bot: Bot):
    """
    Obunani tekshirish callback handleri
    """
    user_id = callback.from_user.id

    if not CHANNELS:
        await callback.answer("✅ Obuna talab qilinmaydi!", show_alert=True)
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass
        return

    not_subscribed_channels = []

    for channel in CHANNELS:
        is_subscribed = await subscription.check(bot=bot, user_id=user_id, channel=channel)

        if not is_subscribed:
            try:
                chat = await bot.get_chat(channel)
                invite_link = chat.invite_link

                if not invite_link:
                    invite_link = await bot.export_chat_invite_link(channel)

                not_subscribed_channels.append((chat.title, invite_link))
            except Exception:
                continue

    if not_subscribed_channels:
        text = "📢 <b>Botdan foydalanish uchun quyidagi kanal(lar)ga obuna bo'ling:</b>"
        keyboard = get_subscription_keyboard(not_subscribed_channels)

        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except TelegramBadRequest:
            pass

        await callback.answer("❌ Siz hali barcha kanallarga obuna bo'lmagansiz!", show_alert=True)
    else:
        await callback.answer("✅ Tabriklaymiz! Siz barcha kanallarga obuna bo'ldingiz!", show_alert=True)

        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass

        await callback.message.answer(
            f"🎉 Xush kelibsiz, {callback.from_user.full_name}!\n\n"
            "Endi botdan to'liq foydalanishingiz mumkin."
        )