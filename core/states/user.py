from aiogram.fsm.state import State, StatesGroup


class HandleUser(StatesGroup):
    codex = State()
    material_type = State()
    search_format = State()
    theme = State()
