import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.filters.role import AdminFilter
from core.keyboards import *
from core.states.admin import *
from services.db.storage import Storage


logger = logging.getLogger(__name__)
admin_router = Router(name=__name__)


@admin_router.message(AdminFilter(), Command("admin"))
async def admin_menu(message: Message, state: FSMContext, store: Storage):
    await message.answer("Админ-панель открыта", reply_markup=get_admin_keyboard())
    await state.clear()
