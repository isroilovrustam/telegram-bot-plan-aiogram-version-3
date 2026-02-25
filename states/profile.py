from aiogram.fsm.state import StatesGroup, State


class UpdateProfile(StatesGroup):
    phone = State()
    full_name = State()

