from aiogram import Dispatcher, Router

from .users import users_router
from .groups import groups_router
from .channels import channels_router
from .errors import errors_router


def setup_routers(dp: Dispatcher) -> None:
    """Barcha routerlarni dispatcherga ulash"""
    dp.include_router(users_router)
    dp.include_router(groups_router)
    dp.include_router(channels_router)
    dp.include_router(errors_router)
