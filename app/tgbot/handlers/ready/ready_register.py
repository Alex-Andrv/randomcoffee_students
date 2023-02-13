from aiogram import Dispatcher

from app.tgbot.handlers.ready.ready_handlers import ReadyStates
from app.tgbot.handlers.ready.edit_handler import edit_profile
from app.tgbot.handlers.ready.start_search import start_conversation


def register_ready(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_conversation,
        text='start_conversation',
        state=ReadyStates.ready)

    dp.register_callback_query_handler(
        edit_profile,
        text='edit_profile',
        state=ReadyStates.ready)
