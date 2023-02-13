from aiogram.dispatcher.filters.state import StatesGroup, State


class ReadyStates(StatesGroup):
    ready = State()
