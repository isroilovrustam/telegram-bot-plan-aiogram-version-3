from aiogram import Router, F
from aiogram.types import Message
from utils.db_api import db

router = Router(name="users_info")


@router.message(F.text == "/users_count")
async def users_count(message: Message):
    try:
        users = await db.count_users()
        await message.answer(f"Foydalanuvchilar soni: {users}")
    except Exception as e:
        await message.answer("Xatolik yuz berdi. Bazada muammo bo'lishi mumkin.")

@router.message(F.text == "/all_profiles")
async def view_all_profiles(message: Message):
    users = await db.get_all_users()

    if not users:
        await message.answer("❌ Bazada hech qanday foydalanuvchi topilmadi.")
        return

    BATCH_SIZE = 10
    for i in range(0, len(users), BATCH_SIZE):
        batch = users[i:i + BATCH_SIZE]  # 10 tadan olib turish

        response = "👥 <b>FOYDALANUVCHILAR PROFILLARI</b>\n"
        response += "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        for idx, user in enumerate(batch, 1):
            response += (
                f"<b>{idx}. {user['full_name']}</b>\n"
                f"🆔 ID: {user['id']}\n"
                f"📲 Telegram ID: <code>{user['telegram_id']}</code>\n"
                f"🔗 Username: @{user.get('username') if user.get('username') else '—'}\n"
                f"📞 Telefon: {user.get('phone') if user.get('phone') else '—'}\n"
                f"📅 Qo'shilgan: {user['created_at']}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            )

        await message.answer(response, parse_mode="HTML")



