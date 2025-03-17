import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core import texts
from core.states import *
from core.keyboards.user import *
from services.db.storage import Storage

logger = logging.getLogger(__name__)
user_router = Router(name=__name__)


@user_router.message(Command("start", "search"))
async def send_start(message: Message, store: Storage, state: FSMContext):
    await message.answer(texts.messages.start, reply_markup=get_start_keyboard())
    await state.clear()
