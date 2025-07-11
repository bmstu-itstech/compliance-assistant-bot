import logging

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import lazyload, joinedload, selectinload

from core import domain
from services.db import models


logger = logging.getLogger(__name__)


class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        super().__init__(f"user not found: {user_id}")


class Storage:
    _db: AsyncSession

    def __init__(self, conn: AsyncSession):
        self._db = conn

    async def create_theme(self, theme: domain.ThemeRecord):
        new_theme = models.Theme.from_domain(theme)
        self._db.add(new_theme)
        await self._db.commit()
        logger.info(f"add theme with id {theme.id}")

    async def create_material(self, material: domain.MaterialRecord, themes: list[domain.ThemeRecord]):
        new_material = models.Material.from_domain(material)
        for theme in themes:
            theme_model = models.Theme.from_domain(theme)
            merged = await self._db.merge(theme_model)  # Если тема уже существует
            new_material.themes.append(merged)
        self._db.add(new_material)
        await self._db.commit()
        logger.info(f"add material with id {material.id}")

    async def materials(self, **filters) -> None | list[domain.MaterialRecord]:
        stmt = select(models.Material)
        for key, value in filters.items():
            if hasattr(models.Material, key):
                stmt = stmt.filter(getattr(models.Material, key) == value)
            else:
                raise ValueError(f"Invalid filter: {key}")
        result = await self._db.execute(stmt)
        materials = result.scalars().all()
        return [material.to_domain() for material in materials]

    async def themes_by_material(self, material_id: int) -> None | list[domain.ThemeRecord]:
        stmt = (
            select(models.Material)
            .where(models.Material.id == material_id)
            .options(selectinload(models.Material.themes))
        )
        result = await self._db.execute(stmt)
        material = result.scalars().first()
        if not material:
            return None
        return [theme.to_domain() for theme in material.themes]

    async def materials_by_theme(self, theme_id: int) -> None | list[domain.MaterialRecord]:
        stmt = (
            select(models.Theme)
            .where(models.Theme.id == theme_id)
            .options(selectinload(models.Theme.materials))
        )
        result = await self._db.execute(stmt)
        theme = result.scalars().first()
        if not theme:
            return None
        return [material.to_domain() for material in theme.materials]

    async def themes_by_partial_title(self, name: str) -> list[domain.ThemeRecord]:
        res = await self._db.execute(
            select(models.Theme).where(models.Theme.name.ilike(f"%{name}%"))
        )
        themes = res.scalars().all()
        return [theme.to_domain() for theme in themes]

    async def theme_by_id(self, theme_id: int) -> domain.ThemeRecord:
        res = await self._db.execute(
            select(models.Theme).where(models.Theme.id == theme_id)
        )
        theme = res.scalars().first()
        return theme.to_domain()

    async def theme_by_name(self, name: str) -> domain.ThemeRecord | None:
        res = await self._db.execute(
            select(models.Theme).where(models.Theme.name == name)
        )
        theme = res.scalars().first()
        if theme is not None:
            return theme.to_domain()
