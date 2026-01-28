from aiogram import Dispatcher

# Filterlar shu yerda import qilinadi
# Masalan:
from .is_admin import IsAdminFilter
from .is_group import IsGroup
from .is_private import IsPrivate


def setup_filters(dp: Dispatcher) -> None:
    """Barcha filterlarni sozlash"""
    # Filterlar shu yerda ro'yxatdan o'tkaziladi
    # Masalan:
    dp.message.filter(IsAdminFilter())
    dp.message.filter(IsGroup())
    dp.message.filter(IsPrivate())
