from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
import re
from keyboards.default.contact_buttons import keyboard
from states.profile import UpdateProfile
from utils.db_api import db

router = Router(name="profile")


@router.message(F.text == "/profile")
async def view_profile(message: Message):
    telegram_id = message.from_user.id

    # Bazadan ma'lumotlarni olish
    user = await db.get_user(telegram_id)

    if not user:
        await message.answer(
            "❌ Sizning profil ma'lumotlaringiz bazada topilmadi.\n"
            "Iltimos, /start komandasi bilan ro'yxatdan o'ting."
        )
        return

    response = "👤 <b>PROFIL MA'LUMOTLARI</b>\n"
    response += "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    response += f"🆔 <b>ID:</b> {user['id']}\n"
    response += f"📲 <b>Telegram ID:</b> <code>{user['telegram_id']}</code>\n"
    response += f"🙍‍♂️ <b>To'liq Ism:</b> {user['full_name']}\n"
    response += f"🔗 <b>Username:</b> @{user.get('username') if user.get('username') else '—'}\n"
    response += f"📞 <b>Telefon:</b> {user.get('phone') if user.get('phone') else '—'}\n"
    response += f"📅 <b>Qo'shilgan Sana:</b> {user['created_at']}\n"
    response += "━━━━━━━━━━━━━━━━━━━━━━━━━"

    await message.answer(response, parse_mode="HTML")


@router.message(F.text == "/update_phone")
async def start_update_phone(message: Message, state: FSMContext):
    await message.answer(
        "Iltimos, yangi telefon raqamingizni kiriting yoki 'Telefon raqamini ulashish' tugmasini bosing.",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await state.set_state(UpdateProfile.phone)


@router.message(UpdateProfile.phone)
async def update_phone(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    phone = None
    if message.contact:
        phone = message.contact.phone_number
    elif message.text:
        phone = message.text.strip()

    if not phone:
        await message.answer("Telefon raqami topilmadi. Iltimos, qaytadan urinib ko'ring.")
        return

    # Agar + bo'lmasa, qo'shish (Uzbekiston raqamlari uchun odatiy)
    if not phone.startswith('+'):
        phone = '+' + phone

    if not re.match(r'^\+\d{9,15}$', phone):
        await message.answer(
            "Noto'g'ri format. Telefon raqami '+' bilan boshlanishi va raqamlardan iborat bo'lishi kerak (masalan, +998901234567).")
        return

    try:
        await db.update_user_phone(telegram_id, phone)
        await message.answer("✅ Telefon raqamingiz yangilandi!", reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        await message.answer("Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")

    await state.clear()


@router.message(F.text == "/update_name")
async def start_update_name(message: Message, state: FSMContext):
    await message.answer(
        "Iltimos, yangi ismingizni kiriting (masalan, Rustamjon Abdullayev).",
        parse_mode="HTML"
    )
    await state.set_state(UpdateProfile.full_name)


@router.message(UpdateProfile.full_name)
async def update_full_name(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    full_name = message.text.strip()

    if not full_name or len(full_name) < 3:
        await message.answer("Ism noto'g'ri yoki juda qisqa. Iltimos, to'liq ismingizni kiriting.")
        return  # State ni saqlab, qayta kiritishga imkon beradi

    try:
        await db.update_user_fullname(telegram_id, full_name)
        await message.answer(f"✅ Ismingiz yangilandi: {full_name}")
    except Exception as e:
        # Logging qilish mumkin: logging.error(e)
        await message.answer("Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")

    await state.clear()


@router.message(F.text == "/delete_profile")
async def confirm_delete_profile(message: Message):
    """Profil o'chirishni tasdiqlash (xavfli!)"""

    telegram_id = message.from_user.id

    # Profilni o'chirish
    await db.delete_user(telegram_id)

    await message.answer(
        "🗑️ <b>Profil O'CHIRILDI</b>\n\n"
        "Sizning barcha ma'lumotlaringiz bazadan o'chirildi.\n"
        "Yana ro'yxatdan o'tish uchun /start ni bosing.",
        parse_mode="HTML"
    )
