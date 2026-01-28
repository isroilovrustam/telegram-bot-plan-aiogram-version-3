from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.enums import ChatType


class IsGroup(BaseFilter):
    """Guruhda ekanligini tekshiruvchi filter"""

    async def __call__(self, message: Message) -> bool:
        return message.chat.type in (
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        )