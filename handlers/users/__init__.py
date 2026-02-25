from aiogram import Router

from .ad import router as ad_router
from .profile import router as profile_router
from .users_information import router as users_info_router
from .start import router as start_router
from .help import router as help_router
from .echo import router as echo_router

users_router = Router(name="users")

# Sub-routerlarni ulash
users_router.include_router(ad_router)
users_router.include_router(profile_router)
users_router.include_router(users_info_router)
users_router.include_router(start_router)
users_router.include_router(help_router)
users_router.include_router(echo_router)
