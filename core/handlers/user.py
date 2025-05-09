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
    await send_material_type(call, state)


async def send_material_type(call, state):
    data = await state.get_data()
    codex = data["codex"]
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
    await state.set_state(HandleUser.material_type)


def map_codex(codex: str) -> domain.Codex:
    if codex == domain.Codex.TAX.value:
        return domain.Codex.TAX
    elif codex == domain.Codex.LABOR.value:
        return domain.Codex.LABOR


@user_router.callback_query(F.data.startswith("material_type"))
async def handle_material_type(call: CallbackQuery, state: FSMContext):
    await call.answer()
    material_type = map_material_type_to_domain("_".join(call.data.split("_")[2:]))
    await state.update_data(material_type=material_type)
    await send_search_format(call, state)
    await state.set_state(HandleUser.search_format)


async def send_search_format(call, state):
    data = await state.get_data()
    await call.message.edit_text(
        texts.messages.choose_search_format.format(
            codex=map_codex_to_str(data["codex"]).lower(),
            material_type=map_material_type_to_str(data["material_type"]),
        ),
        reply_markup=get_search_format_keyboard()
    )


def map_material_type_to_domain(material_type: str) -> domain.MaterialType:
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
        await send_theme_choose(call, state)
        await state.set_state(HandleUser.theme)
        await state.update_data(message_to_update=call.message)


async def send_themes(message, state, store, partial_name: str = None):
    data = await state.get_data()
    materials = await store.materials(codex=data["codex"], material_type=data["material_type"])
    if partial_name:
        themes = list({
            (theme.id, theme.name)
            for material in materials
            for theme in await store.themes_by_material(material.id)
            if partial_name in theme.name
        })
    else:
        themes = list({
            (theme.id, theme.name)
            for material in materials
            for theme in await store.themes_by_material(material.id)
        })
    if not themes:
        await message.edit_text(texts.messages.no_themes)
        return
    await message.edit_text(
        texts.messages.list_themes.format(
            codex=map_codex_to_str(data["codex"]).lower(),
            material_type=map_material_type_to_str(data["material_type"]),
        ), reply_markup=get_themes_keyboard(themes)
    )


async def send_theme_choose(call, state):
    data = await state.get_data()
    await call.message.edit_text(
        texts.messages.enter_theme.format(
            codex=map_codex_to_str(data["codex"]).lower(),
            material_type=map_material_type_to_str(data["material_type"]),
        )
    )


@user_router.message(HandleUser.theme)
async def handle_input_theme(message: Message, store: Storage, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    await send_themes(data["message_to_update"], state, store, message.text)


F: CallbackQuery


@user_router.callback_query(F.data.startswith("theme"))
async def handle_chosen_theme(call: CallbackQuery, state: FSMContext, store: Storage):
    await call.answer()
    theme_id = int(call.data.split("_")[-1])
    theme = await store.theme_by_id(theme_id)
    materials = await store.materials_by_theme(theme_id)
    await send_materials(call, state, materials, theme)


async def send_materials(call, state, materials, theme):
    data = await state.get_data()
    await call.message.edit_text(
        texts.messages.list_materials.format(
            codex=map_codex_to_str(data["codex"]).lower(),
            material_type=map_material_type_to_str(data["material_type"]),
            theme=theme.name,
        ),
        reply_markup=get_materials_keyboard(materials)
    )


@user_router.callback_query(F.data.startswith("material"))
async def handle_material(call: CallbackQuery, store: Storage, state: FSMContext):
    await call.answer()
    material_id = int(call.data.split("_")[-1])
    materials = await store.materials(id=material_id)
    material = materials[0]
    await send_material(call, material)


async def send_material(call, material):
    await call.message.answer(
        f"<i><b>\"{material.name}\"</b></i> "
        f"({map_codex_to_str(material.codex)} кодекс) - {map_material_type_to_str(material.material_type)}\n\n"
        f"<i>{material.description}</i>\n\n"
        f"{material.content}"
    )


@user_router.callback_query(F.data == "back")
async def back(call: CallbackQuery, state: FSMContext, store: Storage):
    await call.answer()
    current_state = await state.get_state()
    if current_state == HandleUser.material_type:
        await call.message.delete()
        await send_codexes(call.message, state)
    elif current_state == HandleUser.search_format:
        await send_material_type(call, state)
    elif current_state == HandleUser.theme:
        await send_themes(call.message, state, store)


def map_material_type_to_str(material_type: domain.MaterialType) -> str:
    if material_type == domain.MaterialType.LAW:
        return "законодательство"
    elif material_type == domain.MaterialType.JUDICIAL_PRACTICE:
        return "судебная практика"
    elif material_type == domain.MaterialType.CASE:
        return "кейс"
    elif material_type == domain.MaterialType.ADVICE:
        return "совет"


def map_codex_to_str(codex: domain.Codex) -> str:
    if codex == domain.Codex.LABOR:
        return "Трудовой"
    elif codex == domain.Codex.TAX:
        return "Налоговый"
