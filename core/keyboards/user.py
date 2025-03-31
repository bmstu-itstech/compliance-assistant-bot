from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core import texts, domain


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


def get_codexes_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="Налоговый комплаенс", callback_data=f"codex_{domain.Codex.TAX}"),
        InlineKeyboardButton(text="Трудовой комплаенс", callback_data=f"codex_{domain.Codex.LABOR}"),
    ]
    builder.max_width = 1
    builder.add(*buttons)
    return builder.as_markup()


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core import texts, domain


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


def get_material_types_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="Законодательство", callback_data=f"material_type_{domain.MaterialType.LAW}"),
        InlineKeyboardButton(text="Судебные практики", callback_data=f"material_type_{domain.MaterialType.JUDICIAL_PRACTICE}"),
        InlineKeyboardButton(text="Кейсы", callback_data=f"material_type_{domain.MaterialType.CASE}"),
        InlineKeyboardButton(text="Советы", callback_data=f"material_type_{domain.MaterialType.ADVICE}"),
    ]
    builder.add(*buttons)
    builder.adjust(2, 2)
    return builder.as_markup()


def get_search_format_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="Из существующих", callback_data="search_format_exist"),
        InlineKeyboardButton(text="Ручной ввод", callback_data="search_format_custom"),
    ]
    builder.max_width = 1
    builder.add(*buttons)
    return builder.as_markup()


def get_themes_keyboard(themes: list[domain.ThemeRecord]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=theme.name, callback_data=f"theme_{theme.id}")
        for theme in themes
    ]
    builder.add(*buttons)
    sizes = [10] * (len(themes) // 10) + [len(themes) % 10]
    if len(themes) > 10:
        builder.add(
            InlineKeyboardButton(text="⬅️Предыдущая", callback_data="prev"),
            InlineKeyboardButton(text="Следующая➡️", callback_data="next"),
        )
        sizes.append(2)
    builder.adjust(*sizes)
    return builder.as_markup()
