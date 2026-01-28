from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_inline_keyboard(items: dict, row_width: int = 2) -> InlineKeyboardMarkup:
    """
    Inline klaviatura yaratish
    
    :param items: {text: callback_data} formatidagi dict
    :param row_width: Qatordagi tugmalar soni
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    for text, callback_data in items.items():
        builder.button(text=text, callback_data=callback_data)
    
    builder.adjust(row_width)
    return builder.as_markup()


def make_url_keyboard(items: dict, row_width: int = 2) -> InlineKeyboardMarkup:
    """
    URL li inline klaviatura yaratish
    
    :param items: {text: url} formatidagi dict
    :param row_width: Qatordagi tugmalar soni
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    
    for text, url in items.items():
        builder.button(text=text, url=url)
    
    builder.adjust(row_width)
    return builder.as_markup()
