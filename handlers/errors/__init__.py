from aiogram import Router

from .error_handler import router as error_router

errors_router = Router(name="errors")
errors_router.include_router(error_router)
