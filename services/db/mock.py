from core import domain
from services.db.storage import Storage

labor_theme_names = (
    "Трудовые отношения, стороны трудовых отношений, основания возникновения трудовых отношений",
    "Социальное партнерство в сфере труда",
    "Трудовой договор",
    "Рабочее время",
    "Время отдыха",
    "Оплата и нормирование труда",
    "Гарантии и компенсации",
    "Трудовой распорядок. Дисциплина труда",
    "Материальная ответственность сторон Трудового договора",
    "Особенности регулирования труда отдельных категорий работников",
)

tax_theme_names = (
    "Налоговый кодекс РФ",
    "Федеральные налоги",
    "Налоговый учет по ОСНО",
    "Налоговые льготы вычеты для малого бизнеса",
    "Специальные налоговые режимы",
    "Законодательные обновления",
    "Выбор налогового режима",
    "Налоговый учет",
    "Управление налоговыми рисками",
)


labor_materials = (

)


async def load_data(store: Storage):
    for theme_name in labor_theme_names + tax_theme_names:
        themes = await store.themes_by_partial_title(theme_name)
        if not themes:
            await store.create_theme(domain.ThemeRecord(id=None, name=theme_name, materials=None))
            themes = await store.themes_by_partial_title(theme_name)
        await store.create_material(
            domain.MaterialRecord(
                id=None,
                name="ТК РФ Статья 15. Трудовые отношения",
                codex=domain.Codex.LABOR,
                material_type=domain.MaterialType.LAW,
                themes=themes,
                content="https://base.garant.ru/12125268/36bfb7176e3e8bfebe718035887e4efc/",
            )
        )
