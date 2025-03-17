import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from services.db.storage import Storage


logger = logging.getLogger(__name__)


class DbMiddleware(BaseMiddleware):

    def __init__(self, pool):
        super().__init__()
        self.pool = pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ):
        async with self.pool() as db:
            data["db"] = db
            data["store"] = Storage(db)
            return await handler(event, data)
