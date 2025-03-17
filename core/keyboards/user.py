from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core import texts


def get_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=texts.buttons.button1, callback_data="button1"),
        InlineKeyboardButton(text=texts.buttons.button2, callback_data="button2"),
        InlineKeyboardButton(text=texts.buttons.button3, callback_data="button3"),
    ]
    builder.add(*buttons)
    builder.adjust(2, 1)
    return builder.as_markup()
