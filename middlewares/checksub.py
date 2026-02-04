import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, CallbackQuery, TelegramObject, Update

from data.config import CHANNELS
from utils.misc import subscription
from keyboards.inline.subscription import get_subscription_keyboard


class CheckSubscriptionMiddleware(BaseMiddleware):
    """
    Majburiy obuna middleware - foydalanuvchilarni kanal(lar)ga obunasini tekshirish
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        # Agar kanallar ro'yxati bo'sh bo'lsa, middleware ni o'tkazib yuboramiz
        if not CHANNELS:
            return await handler(event, data)

        bot: Bot = data.get("bot")
        user_id = None

        # Message uchun
        if isinstance(event, Message):
            user_id = event.from_user.id

            # /start va /help buyruqlarini tekshirmasdan o'tkazamiz
            if event.text and event.text in ['/start', '/help']:
                return await handler(event, data)

        # CallbackQuery uchun
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id

            # check_subs callback ni tekshirmasdan o'tkazamiz
            if event.data == "check_subs":
                return await handler(event, data)

        else:
            # Boshqa turdagi eventlarni o'tkazib yuboramiz
            return await handler(event, data)

        # Agar user_id aniqlanmagan bo'lsa
        if user_id is None:
            return await handler(event, data)

        # Obunani tekshirish
        not_subscribed_channels = []

        for channel in CHANNELS:
            is_subscribed = await subscription.check(bot=bot, user_id=user_id, channel=channel)

            if not is_subscribed:
                try:
                    chat = await bot.get_chat(channel)
                    invite_link = chat.invite_link

                    # Agar invite_link bo'lmasa, yangi yaratamiz
                    if not invite_link:
                        invite_link = await bot.export_chat_invite_link(channel)

                    not_subscribed_channels.append((chat.title, invite_link))
                except Exception as e:
                    logging.error(f"Kanal ma'lumotlarini olishda xatolik: {e}")
                    continue

        # Agar obuna bo'lmagan kanallar bo'lsa
        if not_subscribed_channels:
            text = "📢 <b>Botdan foydalanish uchun quyidagi kanal(lar)ga obuna bo'ling:</b>"
            keyboard = get_subscription_keyboard(not_subscribed_channels)

            if isinstance(event, Message):
                await event.answer(text, reply_markup=keyboard)
            elif isinstance(event, CallbackQuery):
                await event.message.answer(text, reply_markup=keyboard)
                await event.answer("❌ Siz hali barcha kanallarga obuna bo'lmagansiz!", show_alert=True)

            # Handler ni chaqirmaymiz (CancelHandler o'rniga)
            return

        # Barcha kanallarga obuna bo'lgan bo'lsa, handler ni chaqiramiz
        return await handler(event, data)
