from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router(name="echo")


# Echo bot - barcha xabarlarga javob beradi (state bo'lmaganda)
@router.message(F.text)
async def bot_echo(message: Message, state: FSMContext):
    """
    Echo handler - foydalanuvchi xabarini qaytaradi
    Bu handler eng oxirida bo'lishi kerak!
    """
    # Agar state bo'lsa, echo qilmaymiz
    current_state = await state.get_state()
    if current_state is not None:
        return
    
    await message.answer(message.text)
