from aiogram.dispatcher.filters.state import StatesGroup, State


class ReadyStates(StatesGroup):
    ready = State()
    edit_profile = State()
    add_to_queue = State()
