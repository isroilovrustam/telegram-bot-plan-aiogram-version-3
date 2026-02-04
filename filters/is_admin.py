from aiogram.filters import BaseFilter
from aiogram.types import Message

from data.config import ADMINS


class IsAdminFilter(BaseFilter):
    """
    Admin ekanligini tekshiruvchi filter
    """
    
    async def __call__(self, message: Message) -> bool:
        """
        Foydalanuvchi admin ekanligini tekshirish
        """
        return str(message.from_user.id) in ADMINS
