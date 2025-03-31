import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core import texts
from core.states.user import *
from core.keyboards.user import *
from services.db.storage import Storage

logger = logging.getLogger(__name__)
user_router = Router(name=__name__)


@user_router.message(Command("start"))
async def send_start(message: Message, state: FSMContext):
    await message.answer(texts.messages.start)
    await send_codexes(message, state)
    await state.clear()


async def send_codexes(message: Message, state: FSMContext):
    await message.answer(texts.messages.choose_codexes, reply_markup=get_codexes_keyboard())
    await state.set_state(HandleUser.codex)


F: CallbackQuery


@user_router.callback_query(F.data.startswith("codex"))
async def handle_codex(call: CallbackQuery, state: FSMContext):
    await call.answer()
    codex = map_codex(call.data.split("_")[-1])
    await state.update_data(codex=codex)
    await send_material_type(call, codex)
    await state.set_state(HandleUser.material_type)


async def send_material_type(call, codex):
    if codex is domain.Codex.TAX:
        await call.message.edit_text(
            texts.messages.tax_codex,
            reply_markup=get_material_types_keyboard(),
            disable_web_page_preview=True,
        )
    elif codex is domain.Codex.LABOR:
        await call.message.edit_text(
            texts.messages.labor_codex,
            reply_markup=get_material_types_keyboard(),
            disable_web_page_preview=True,
        )


def map_codex(codex: str) -> domain.Codex:
    if codex == domain.Codex.TAX.value:
        return domain.Codex.TAX
    elif codex == domain.Codex.LABOR.value:
        return domain.Codex.LABOR


@user_router.callback_query(F.data.startswith("material_type"))
async def handle_material_type(call: CallbackQuery, state: FSMContext):
    await call.answer()
    material_type = map_material_type(call.data.split("_")[-1])
    await state.update_data(material_type=material_type)
    await send_search_format(call)
    await state.set_state(HandleUser.search_format)


async def send_search_format(call):
    await call.message.edit_text(texts.messages.choose_search_format, reply_markup=get_search_format_keyboard())


def map_material_type(material_type: str) -> domain.MaterialType:
    if material_type == domain.MaterialType.LAW.value:
        return domain.MaterialType.LAW
    elif material_type == domain.MaterialType.JUDICIAL_PRACTICE.value:
        return domain.MaterialType.JUDICIAL_PRACTICE
    elif material_type == domain.MaterialType.CASE.value:
        return domain.MaterialType.CASE
    elif material_type == domain.MaterialType.ADVICE.value:
        return domain.MaterialType.ADVICE


@user_router.callback_query(F.data.startswith("search_format"))
async def handle_search_format(call: CallbackQuery, store: Storage, state: FSMContext):
    await call.answer()
    search_format = call.data.split("_")[-1]
    if search_format == "exist":
        await send_themes(call.message, state, store)
    if search_format == "custom":
        await send_theme_choose(call)
        await state.set_state(HandleUser.theme)


async def send_themes(message, state, store, partial_name: str = None):
    data = await state.get_data()
    materials = await store.materials(codex=data["codex"], material_type=data["material_type"])
    if partial_name:
        themes = list({material.theme for material in materials if partial_name in material.theme.name})
    else:
        themes = list({material.theme for material in materials})
    await message.edit_text(texts.messages.list_themes, reply_markup=get_themes_keyboard(themes))


async def send_theme_choose(call):
    await call.message.edit_text(texts.messages.enter_theme)


@user_router.message(HandleUser.theme)
async def handle_theme(message: Message, store: Storage, state: FSMContext):
    await send_themes(message, state, store, message.text)
