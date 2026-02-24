import asyncio

from aiogram import Router, F
from aiogram.exceptions import TelegramRetryAfter, TelegramForbiddenError
from aiogram.types import Message

from utils.db_api import db
router = Router(name="ad")


@router.message(F.text == "/allusers")
async def all_users(message: Message):
    # Get all users asynchronously
    users = await db.get_all_users()  # Note: await is needed since get_all_users is async

    if not users:
        await message.answer("No users found in the database.")
        return

    BATCH_SIZE = 10
    for i in range(0, len(users), BATCH_SIZE):
        batch = users[i:i + BATCH_SIZE]

        response = "👥 <b>Users List</b>\n"
        response += "━━━━━━━━━━━━━━━━━━\n\n"

        for user in batch:
            response += (
                f"🆔 <b>ID:</b> {user['id']}\n"
                f"📲 <b>Telegram ID:</b> {user['telegram_id']}\n"
                f"🙍‍♂️ <b>Name:</b> {user['full_name']}\n"
                f"🔗 <b>Username:</b> @{user.get('username') if user.get('username') else '—'}\n"
                f"📞 <b>Phone:</b> {user.get('phone') if user.get('phone') else '—'}\n"
                f"📅 <b>Created:</b> {user['created_at']}\n"
                f"━━━━━━━━━━━━━━━━━━\n\n"
            )

        await message.answer(response, parse_mode="HTML")


@router.message(F.text == "/send_ad")
async def send_ad_to_all_users(message: Message):
    # Get all users asynchronously
    users = await db.get_all_users()  # Note: await is needed since get_all_users is async

    if not users:
        await message.answer("No users found in the database.")
        return

    ad_text = "Bu reklama xabari! 😊"  # Replace with your actual ad text or make it dynamic

    sent_count = 0
    blocked_count = 0
    error_count = 0

    for user in users:
        try:
            await message.bot.send_message(chat_id=user['telegram_id'], text=ad_text)
            sent_count += 1
            # Rate limit: Telegram allows ~30 messages per second to different users
            await asyncio.sleep(1 / 30)  # ~33ms delay to stay under 30 msg/sec
        except TelegramForbiddenError:
            # User has blocked the bot, delete from database
            await db.delete_user(user['telegram_id'])
            blocked_count += 1
        except TelegramRetryAfter as e:
            error_count += 1
        except Exception as e:
            error_count += 1

    response = f"Reklama yuborildi:\n- Muvaffaqiyatli: {sent_count}\n- Bloklaganlar (o'chirildi): {blocked_count}\n- Xatolar: {error_count}"
    await message.answer(response)