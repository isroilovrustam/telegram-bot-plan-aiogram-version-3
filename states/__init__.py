from aiogram.fsm.state import State, StatesGroup


# Misol uchun State
class UserState(StatesGroup):
    """
    Foydalanuvchi holati
    """
    name = State()  # Ism kiritish
    age = State()   # Yosh kiritish
    phone = State()  # Telefon raqam kiritish


# Boshqa statelar shu yerga qo'shiladi
