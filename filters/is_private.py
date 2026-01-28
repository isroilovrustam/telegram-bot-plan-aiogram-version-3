from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.enums import ChatType


class IsPrivate(BaseFilter):
    """Shaxsiy chatda ekanligini tekshiruvchi filter"""

    async def __call__(self, message: Message) -> bool:
        return message.chat.type == ChatType.PRIVATE