from sys import stderr

import pandas as pd
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.domain import Codex, MaterialRecord, MaterialType, ThemeRecord
from core.filters.role import AdminFilter
from services.db.storage import Storage


admin_router = Router(name=__name__)

CODEX_MAPPING = {
    "Налоговый": Codex.TAX,
    "Трудовой": Codex.LABOR
}

MATERIAL_TYPE_MAPPING = {
    "Закон": MaterialType.LAW,
    "Судебная практика": MaterialType.JUDICIAL_PRACTICE,
    "Кейс": MaterialType.CASE,
    "Совет": MaterialType.ADVICE
}


@admin_router.message(AdminFilter(), Command("upload"))
async def upload(message: Message, state: FSMContext, store: Storage):
    await message.answer("Отправьте файл с данными")
    await state.clear()


@admin_router.message(AdminFilter(), F.document)
async def handle_uploaded_file(message: Message, store: Storage):
    if message.document.mime_type not in (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel"
    ):
        await message.answer("Пожалуйста, отправьте файл в формате Excel (.xlsx)")
        return

    try:
        file = await message.bot.get_file(message.document.file_id)
        file_path = file.file_path
        file_bytes = await message.bot.download_file(file_path)

        df = pd.read_excel(file_bytes, sheet_name="Материалы")

        required_columns = ['Название', 'Кодекс', 'Тип', 'Контент']
        if not all(col in df.columns for col in required_columns):
            missing = [col for col in required_columns if col not in df.columns]
            await message.answer(f"В файле отсутствуют обязательные колонки: {', '.join(missing)}")
            return

        for _, row in df.iterrows():
            try:
                name = str(row['Название']).strip()
                if not name:
                    raise ValueError("Название не может быть пустым")

                description = str(row['Описание']).strip() if 'Описание' in df.columns and pd.notna(
                    row['Описание']) else None

                codex_str = str(row['Кодекс']).strip()
                if codex_str not in CODEX_MAPPING:
                    valid_values = ", ".join(CODEX_MAPPING.keys())
                    raise ValueError(f"Некорректный кодекс. Допустимые значения: {valid_values}")
                codex = CODEX_MAPPING[codex_str]

                type_str = str(row['Тип']).strip()
                if type_str not in MATERIAL_TYPE_MAPPING:
                    valid_values = ", ".join(MATERIAL_TYPE_MAPPING.keys())
                    raise ValueError(f"Некорректный тип материала. Допустимые значения: {valid_values}")
                material_type = MATERIAL_TYPE_MAPPING[type_str]

                content = str(row['Контент']).strip()
                if not content:
                    raise ValueError("Контент не может быть пустым")

                themes = []
                if 'Темы' in df.columns and pd.notna(row['Темы']):
                    theme_names = [t.strip() for t in str(row['Темы']).split('|') if t.strip()]
                    for theme_name in theme_names:
                        existing_theme = await store.theme_by_name(theme_name)
                        if not existing_theme:
                            theme = ThemeRecord(id=None, name=theme_name)
                            await store.create_theme(theme)
                            existing_theme = await store.theme_by_name(theme_name)
                        themes.append(existing_theme)

                material = MaterialRecord(
                    id=None,
                    name=name,
                    description=description,
                    codex=codex,
                    material_type=material_type,
                    content=content
                )

                await store.create_material(material, themes)

            except Exception:
                await message.answer(f"Ошибка при обработке строки")
                continue

        await message.answer("Файл успешно обработан и данные сохранены")

    except Exception as e:
        print(e, file=stderr)
        await message.answer(f"Произошла ошибка при обработке файла")
        raise e
