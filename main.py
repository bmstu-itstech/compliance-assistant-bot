import os
import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand
from sqlalchemy.orm import sessionmaker

from common.repository import bot, dp, config
from core.handlers.user import user_router
from core.middlewares.db import DbMiddleware
from core.middlewares.user_control import UserControlMiddleware
from core.texts.commands import commands
from services.db.db_pool import create_db_pool
from core.handlers.admin import admin_router


logger = logging.getLogger(__name__)


async def set_commands(bot: Bot, commands: dict[str, str]) -> None:
    await bot.set_my_commands([
        BotCommand(command=command, description=desc)
        for command, desc in commands.items()
    ])


async def main():
    if os.path.isfile('bot.log'):
        os.remove('bot.log')

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        encoding="UTF-8",
        handlers=[
            logging.FileHandler("bot.log"),
            logging.StreamHandler()
        ]
    )
    logger.info("Starting bot")

    db_pool: sessionmaker = await create_db_pool(
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,
        name=config.db.name,
        echo=False,
    )

    bot_obj = await bot.get_me()
    logger.info(f"Bot username: {bot_obj.username}")
    dp.message.outer_middleware(DbMiddleware(db_pool))
    dp.callback_query.outer_middleware(DbMiddleware(db_pool))

    dp.message.outer_middleware(UserControlMiddleware())
    dp.callback_query.outer_middleware(UserControlMiddleware())

    dp.include_router(admin_router)
    dp.include_router(user_router)

    await set_commands(bot, commands)

    try:
        await dp.start_polling(bot, allowed_updates=["any"])
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
