import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class ThrottlingMiddleware(BaseMiddleware):
    """
    Antiflood middleware - foydalanuvchilarni cheklash
    """
    
    def __init__(self, limit: float = 0.5):
        """
        :param limit: So'rovlar orasidagi minimal vaqt (soniyalarda)
        """
        self.limit = limit
        self.users: Dict[int, float] = {}
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Faqat Message uchun throttling qilamiz
        if not isinstance(event, Message):
            return await handler(event, data)
        
        user_id = event.from_user.id
        current_time = time.time()
        
        # Foydalanuvchi oldin so'rov yuborgan bo'lsa
        if user_id in self.users:
            last_time = self.users[user_id]
            time_passed = current_time - last_time
            
            # Agar limit vaqtidan kam bo'lsa
            if time_passed < self.limit:
                # Birinchi marta ogohlantiramiz
                if time_passed < self.limit / 2:
                    await event.reply("⚠️ Iltimos, sekinroq yozing!")
                return  # Handler ni chaqirmaymiz
        
        # Vaqtni yangilaymiz
        self.users[user_id] = current_time
        
        # Handler ni chaqiramiz
        return await handler(event, data)
