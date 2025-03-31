import logging

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import lazyload

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

    async def create_material(self, material: domain.MaterialRecord):
        new_material = models.Material.from_domain(material)
        self._db.add(material)
        await self._db.commit()
        logger.info(f"add material with id {material.id}")

    # async def user(self, _id: int) -> domain.User | None:
    #     stmt = select(models.User).filter_by(id=_id)
    #     result = await self._db.execute(stmt)
    #     model = result.scalar_one_or_none()
    #     if not model:
    #         raise UserNotFoundException(_id)
    #     return model.to_domain()

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

    async def themes_by_partial_title(self, name: str) -> list[domain.ThemeRecord]:
        res = await self._db.execute(
            select(models.Theme).options(lazyload(models.Theme.materials)).where(models.Theme.name.contains(name))
        )
        themes = res.scalars().all()
        return [theme.to_domain() for theme in themes]

    # async def update_user(self, user_id: int, **kwargs) -> None:
    #     stmt = update(models.User).filter_by(id=user_id).values(**kwargs)
    #     await self._db.execute(stmt)
    #     await self._db.commit()
