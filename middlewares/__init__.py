from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .checksub import CheckSubscriptionMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    """Barcha middlewarelarni sozlash"""
    # Majburiy obuna middleware (birinchi bo'lishi kerak)
    dp.message.middleware(CheckSubscriptionMiddleware())
    dp.callback_query.middleware(CheckSubscriptionMiddleware())

    # Throttling middleware
    dp.message.middleware(ThrottlingMiddleware(limit=0.5))
