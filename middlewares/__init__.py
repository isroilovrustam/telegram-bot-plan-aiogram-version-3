from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    """Barcha middlewarelarni sozlash"""
    # Throttling middleware
    dp.message.middleware(ThrottlingMiddleware(limit=0.5))
