import logging
from aiogram import Router
from aiogram.types import Update
from aiogram.exceptions import (
    TelegramAPIError,
    TelegramBadRequest,
    TelegramNetworkError,
    TelegramForbiddenError,
    TelegramUnauthorizedError,
    TelegramRetryAfter,
    TelegramNotFound,
)

router = Router(name="error_handler")


@router.errors()
async def errors_handler(update: Update, exception: Exception):
    """
    Exceptions handler. Barcha xatolarni ushlaydi.
    """
    
    if isinstance(exception, TelegramBadRequest):
        # Noto'g'ri so'rovlar
        if "message is not modified" in str(exception):
            logging.exception("Message is not modified")
            return True
        if "message to delete not found" in str(exception):
            logging.exception("Message to delete not found")
            return True
        if "message can't be deleted" in str(exception):
            logging.exception("Message can't be deleted")
            return True
        if "message text is empty" in str(exception):
            logging.exception("Message text is empty")
            return True
        if "query is too old" in str(exception):
            logging.exception("Callback query is too old")
            return True
        logging.exception(f"TelegramBadRequest: {exception}\nUpdate: {update}")
        return True
    
    if isinstance(exception, TelegramForbiddenError):
        # Bot bloklangan yoki ruxsat yo'q
        logging.exception(f"TelegramForbiddenError: {exception}")
        return True
    
    if isinstance(exception, TelegramNotFound):
        # Chat yoki xabar topilmadi
        logging.exception(f"TelegramNotFound: {exception}")
        return True
    
    if isinstance(exception, TelegramUnauthorizedError):
        # Token noto'g'ri
        logging.exception(f"TelegramUnauthorizedError: {exception}")
        return True
    
    if isinstance(exception, TelegramRetryAfter):
        # Rate limit
        logging.exception(f"TelegramRetryAfter: {exception}\nUpdate: {update}")
        return True
    
    if isinstance(exception, TelegramNetworkError):
        # Tarmoq xatosi
        logging.exception(f"TelegramNetworkError: {exception}\nUpdate: {update}")
        return True
    
    if isinstance(exception, TelegramAPIError):
        # Boshqa Telegram API xatolari
        logging.exception(f"TelegramAPIError: {exception}\nUpdate: {update}")
        return True
    
    # Boshqa barcha xatolar
    logging.exception(f"Update: {update}\nException: {exception}")
    return True
