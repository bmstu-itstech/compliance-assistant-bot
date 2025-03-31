import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from config import config
from core import domain
from core.domain import Role
from services.db.storage import Storage, UserNotFoundException

logger = logging.getLogger(__name__)


class UserControlMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ):
        if event is not None and not event.from_user.is_bot:
            this_user = event.from_user
        else:
            return

        data["role"] = role_mapper(this_user)
        return await handler(event, data)


def role_mapper(user: User):
    return Role.ADMIN if user.id in config.tg_bot.admin_ids else Role.USER
