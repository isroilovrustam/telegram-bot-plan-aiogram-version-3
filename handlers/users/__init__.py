from aiogram import Router

from .start import router as start_router
from .help import router as help_router
from .echo import router as echo_router

users_router = Router(name="users")

# Sub-routerlarni ulash
users_router.include_router(start_router)
users_router.include_router(help_router)
users_router.include_router(echo_router)
