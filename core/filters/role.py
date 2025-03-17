import typing
import logging

from aiogram.types import User
from aiogram.filters import Filter
from aiogram.types.base import TelegramObject

from core.domain import Role


logger = logging.getLogger(__name__)


class RoleFilter(Filter):
    key = "role"

    def __init__(self, role: typing.Union[None, Role, typing.Collection[Role]] = None):
        if role is None:
            self.roles = None
        elif isinstance(role, Role):
            self.roles = {role}
        else:
            self.roles = set(role)

    async def __call__(
        self,
        obj: TelegramObject,
        role: Role,             # getting role from middleware
    ):
        if self.roles is None:
            return True

        return role in self.roles


class AdminFilter(RoleFilter):
    def __init__(self):
        super().__init__(Role.ADMIN)
