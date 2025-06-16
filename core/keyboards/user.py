import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core import texts, domain


logger = logging.getLogger(name=__name__)


def get_codexes_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="Налоговый комплаенс", callback_data=f"codex_{domain.Codex.TAX}"),
        InlineKeyboardButton(text="Трудовой комплаенс", callback_data=f"codex_{domain.Codex.LABOR}"),
    ]
    builder.max_width = 1
    builder.add(*buttons)
    return builder.as_markup()


def get_material_types_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="Законодательство", callback_data=f"material_type_{domain.MaterialType.LAW}"),
        # Требование заказчика убрать :(
        #InlineKeyboardButton(text="Судебные практики", callback_data=f"material_type_{domain.MaterialType.JUDICIAL_PRACTICE}"),
        InlineKeyboardButton(text="Судебные практики", callback_data=f"noop"),
        InlineKeyboardButton(text="Новости", callback_data=f"material_type_{domain.MaterialType.NEWS}"),
        InlineKeyboardButton(text="Рекомендации", callback_data=f"material_type_{domain.MaterialType.ADVICE}"),
        InlineKeyboardButton(text="Назад", callback_data="back"),
    ]
    builder.add(*buttons)
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def get_search_format_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="Из существующих", callback_data="search_format_exist"),
        # Требование заказчика убрать :(
        #InlineKeyboardButton(text="Ручной ввод", callback_data="search_format_custom"),
        InlineKeyboardButton(text="Назад", callback_data="back"),
    ]
    builder.max_width = 1
    builder.add(*buttons)
    return builder.as_markup()


def get_themes_keyboard(themes: list[tuple[int, str]], offset: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=theme[1], callback_data=f"theme_{theme[0]}")
        for theme in themes[offset:offset + 10]
    ]
    builder.add(*buttons)
    navigation_buttons = []
    if len(themes) > 10:
        navigation_buttons.extend([
            InlineKeyboardButton(text="⬅️ Предыдущая", callback_data="prev"),
            InlineKeyboardButton(text="Следующая ➡️", callback_data="next"),
        ])
    navigation_buttons.append(InlineKeyboardButton(text="Назад", callback_data="back"))
    builder.add(*navigation_buttons)
    if len(themes) > 10:
        builder.adjust(*([1] * len(buttons) + [2, 1]))
    else:
        builder.adjust(*([1] * len(buttons) + [1]))
    return builder.as_markup()


def get_materials_keyboard(materials: list[domain.MaterialRecord], offset: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=material.name, callback_data=f"material_{material.id}")
        for material in materials[offset:offset + 10]
    ]
    builder.add(*buttons)
    navigation_buttons = []
    if len(materials) > 10:
        navigation_buttons.extend([
            InlineKeyboardButton(text="⬅️ Предыдущая", callback_data="prev"),
            InlineKeyboardButton(text="Следующая ➡️", callback_data="next"),
        ])
    navigation_buttons.append(InlineKeyboardButton(text="Назад", callback_data="back"))
    builder.add(*navigation_buttons)
    if len(materials) > 10:
        builder.adjust(*([1] * len(buttons)), 2, 1)
    else:
        builder.adjust(*([1] * len(buttons)), 1)
    return builder.as_markup()
