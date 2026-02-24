from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

# ┌──────────────────────────────────────────────────────────┐
# │  🆕 Database import                                      │
# │  Istalgan handlerda shu bitta qator yozib db ishlatamiz  │
# └──────────────────────────────────────────────────────────┘
from utils.db_api import db

router = Router(name="start")


@router.message(CommandStart())
async def bot_start(message: Message):
    """
    /start buyrug'i uchun handler.

    Foydalanuvchi /start bosganda:
    1. Bazada borligini tekshiramiz
    2. Yo'q bo'lsa — bazaga qo'shamiz
    3. Bor bo'lsa — ismini yangilaymiz (balki o'zgartirgandir)
    """

    # ── message.from_user dan ma'lumotlar olish ──
    telegram_id = message.from_user.id          # Telegram ID (masalan: 123456789)
    full_name = message.from_user.full_name      # To'liq ism (masalan: "Ali Valiyev")
    username = message.from_user.username         # @username (None bo'lishi mumkin)

    # ── Bazada borligini tekshirish ──
    user_exists = await db.user_exists(telegram_id)

    if not user_exists:
        # ── YANGI foydalanuvchi — bazaga qo'shish ──
        await db.add_user(
            telegram_id=telegram_id,
            full_name=full_name,
            username=username,
        )

        # Jami foydalanuvchilar sonini olish
        total = await db.count_users()

        await message.answer(
            f"👋 Xush kelibsiz, <b>{full_name}</b>!\n\n"
            f"Siz muvaffaqiyatli ro'yxatdan o'tdingiz.\n"
            f"📊 Jami foydalanuvchilar: <b>{total}</b>"
        )
    else:
        # ── MAVJUD foydalanuvchi — ismini yangilaymiz ──
        await db.update_user_fullname(telegram_id, full_name)

        await message.answer(
            f"👋 Salom, <b>{full_name}</b>!\n\n"
            f"Siz allaqachon ro'yxatdan o'tgansiz."
        )