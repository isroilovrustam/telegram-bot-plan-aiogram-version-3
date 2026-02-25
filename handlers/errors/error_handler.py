import logging
from aiogram import Router
from aiogram.types import ErrorEvent
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
async def errors_handler(event: ErrorEvent):
    """
    Exceptions handler. Barcha xatolarni ushlaydi.

    ⚠️ Aiogram 3.x da @router.errors() handleri
    ErrorEvent obyektini qabul qiladi.
    Eski usul (update, exception) ISHLAMAYDI!
    """
    exception = event.exception
    update = event.update

    if isinstance(exception, TelegramBadRequest):
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
        logging.exception(f"TelegramForbiddenError: {exception}")
        return True

    if isinstance(exception, TelegramNotFound):
        logging.exception(f"TelegramNotFound: {exception}")
        return True

    if isinstance(exception, TelegramUnauthorizedError):
        logging.exception(f"TelegramUnauthorizedError: {exception}")
        return True

    if isinstance(exception, TelegramRetryAfter):
        logging.exception(f"TelegramRetryAfter: {exception}\nUpdate: {update}")
        return True

    if isinstance(exception, TelegramNetworkError):
        logging.exception(f"TelegramNetworkError: {exception}\nUpdate: {update}")
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f"TelegramAPIError: {exception}\nUpdate: {update}")
        return True

    logging.exception(f"Update: {update}\nException: {exception}")
    return True