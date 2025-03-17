import logging

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def create_user(self, user: domain.User) -> domain.User:
        new_user = models.User.from_domain(user)
        self._db.add(new_user)
        await self._db.commit()
        logger.info(f"add user with id {new_user.id}")
        return new_user

    async def user(self, _id: int) -> domain.User | None:
        stmt = select(models.User).filter_by(id=_id)
        result = await self._db.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise UserNotFoundException(_id)
        return model.to_domain()

    async def users_by(self, count: int = 1, **filters) -> None | domain.User | list[domain.User]:
        """
        Returns all users that match the given filters.
        :param count: -1 if you want all users
        :param filters:
        :return:
        """
        stmt = select(models.User)
        for key, value in filters.items():
            if hasattr(models.User, key):
                stmt = stmt.filter(getattr(models.User, key) == value)
            else:
                raise ValueError(f"Invalid filter: {key}")
        if count != -1:
            stmt = stmt.limit(count)
        result = await self._db.execute(stmt)
        users = result.scalars().all()
        if count == 1 and users:
            return users[0].to_domain()
        return [user.to_domain() for user in users]

    async def amount_users_by(self, **filters) -> int:
        stmt = select(func.count(models.User.id))
        for key, value in filters.items():
            if hasattr(models.User, key):
                stmt = stmt.filter(getattr(models.User, key) == value)
            else:
                raise ValueError(f"Invalid filter: {key}")
        result = await self._db.execute(stmt)
        return result.scalar_one()

    async def update_user(self, user_id: int, **kwargs) -> None:
        stmt = update(models.User).filter_by(id=user_id).values(**kwargs)
        await self._db.execute(stmt)
        await self._db.commit()
