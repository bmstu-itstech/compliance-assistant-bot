import logging
from typing import List, Dict
from core import domain
from services.db.storage import Storage


logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self, store: Storage):
        self.store = store

    async def _get_or_create_theme(self, theme_data: Dict) -> domain.ThemeRecord:
        theme_name = theme_data["name"]

        existing = await self.store.themes_by_partial_title(theme_name)
        if existing:
            return existing[0]

        new_theme = await self.store.create_theme(
            domain.ThemeRecord(id=None, name=theme_name)
        )
        return new_theme

    async def load_themes(self, themes_data: List[Dict]):
        for theme_data in themes_data:
            try:
                theme = await self._get_or_create_theme(theme_data)
                logger.info(f"Theme processed: {theme.name}")
            except Exception as e:
                logger.error(f"Error loading theme {theme_data['name']}: {str(e)}")

    async def load_materials(self, materials_data: List[Dict]):
        for material_data in materials_data:
            try:
                existing_materials = await self.store.materials(name=material_data["name"])
                if existing_materials:
                    logger.info(f"Material already exists, skipping: {material_data['name']}")
                    continue

                theme_records = []
                for theme_name in material_data.get("themes", []):
                    theme = await self._get_or_create_theme({"name": theme_name})
                    theme_records.append(theme)

                material = domain.MaterialRecord(
                    id=None,
                    name=material_data["name"],
                    description=material_data.get("description"),
                    codex=material_data["codex"],
                    material_type=material_data["type"],
                    content=material_data["content"]
                )

                await self.store.create_material(material, themes=theme_records)
                logger.info(f"Material created: {material.name}")

            except Exception as e:
                logger.info(f"Error loading material {material_data.get('name')}: {str(e)}")

    async def load_all(self, themes_data: List[Dict], materials_data: List[Dict]):
        logger.info("Starting data loading...")
        await self.load_themes(themes_data)
        await self.load_materials(materials_data)
        logger.info("Data loading completed")
