from typing import Union

from aiogram import Bot
from aiogram.enums import ChatMemberStatus


async def check(bot: Bot, user_id: int, channel: Union[int, str]) -> bool:
    """
    Foydalanuvchining kanalga obuna bo'lganligini tekshirish

    :param bot: Bot obyekti
    :param user_id: Foydalanuvchi ID si
    :param channel: Kanal ID yoki username
    :return: True agar obuna bo'lsa, False aks holda
    """
    try:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        # Quyidagi statuslar obuna hisoblanadi
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR
        ]
    except Exception:
        # Xatolik bo'lsa (masalan, kanal topilmasa) False qaytaramiz
        return False
