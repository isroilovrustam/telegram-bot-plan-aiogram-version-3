from aiogram import Router
from .start import router as start_router
from .service import router as service_router
from .moderator import router as moderator_router
from .edit import router as edit_router

groups_router = Router(name="groups")
# Bu yerga guruhlar uchun handlerlar qo'shiladi
# Masalan:
# from .some_handler import router as some_router
# groups_router.include_router(some_router)

groups_router.include_router(start_router)
groups_router.include_router(service_router)
groups_router.include_router(moderator_router)
groups_router.include_router(edit_router)
