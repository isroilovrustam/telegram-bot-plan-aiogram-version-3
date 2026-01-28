from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def make_keyboard(items: list, row_width: int = 2) -> ReplyKeyboardMarkup:
    """
    Oddiy klaviatura yaratish
    
    :param items: Tugmalar ro'yxati
    :param row_width: Qatordagi tugmalar soni
    :return: ReplyKeyboardMarkup
    """
    keyboard = []
    row = []
    
    for item in items:
        row.append(KeyboardButton(text=str(item)))
        if len(row) >= row_width:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Klaviaturani olib tashlash
remove_keyboard = ReplyKeyboardRemove()
