import logging
from aiogram import Router, F
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


@router.error(F.update.message.as_("message"))
async def message_error_handler(event: ErrorEvent):
    """
    Message xatolarini ushlash
    """
    return await handle_error(event)


@router.error(F.update.callback_query.as_("callback"))
async def callback_error_handler(event: ErrorEvent):
    """
    Callback query xatolarini ushlash
    """
    return await handle_error(event)


@router.error()
async def global_error_handler(event: ErrorEvent):
    """
    Barcha xatolarni ushlash (global)
    """
    return await handle_error(event)


async def handle_error(event: ErrorEvent) -> bool:
    """
    Xatolarni qayta ishlash
    """
    exception = event.exception
    update = event.update

    if isinstance(exception, TelegramBadRequest):
        if "message is not modified" in str(exception):
            return True
        if "message to delete not found" in str(exception):
            logging.warning("Message to delete not found")
            return True
        if "message can't be deleted" in str(exception):
            logging.warning("Message can't be deleted")
            return True
        if "message text is empty" in str(exception):
            logging.warning("Message text is empty")
            return True
        if "query is too old" in str(exception):
            logging.warning("Callback query is too old")
            return True
        logging.exception(f"TelegramBadRequest: {exception}\nUpdate: {update}")
        return True

    if isinstance(exception, TelegramForbiddenError):
        logging.warning(f"TelegramForbiddenError: {exception}")
        return True

    if isinstance(exception, TelegramNotFound):
        logging.warning(f"TelegramNotFound: {exception}")
        return True

    if isinstance(exception, TelegramUnauthorizedError):
        logging.error(f"TelegramUnauthorizedError: {exception}")
        return True

    if isinstance(exception, TelegramRetryAfter):
        logging.warning(f"TelegramRetryAfter: {exception}\nUpdate: {update}")
        return True

    if isinstance(exception, TelegramNetworkError):
        logging.error(f"TelegramNetworkError: {exception}\nUpdate: {update}")
        return True

    if isinstance(exception, TelegramAPIError):
        logging.error(f"TelegramAPIError: {exception}\nUpdate: {update}")
        return True

    logging.exception(f"Update: {update}\nException: {exception}")
    return True