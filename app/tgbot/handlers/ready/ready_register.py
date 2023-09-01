from aiogram import Dispatcher

from app.tgbot.handlers.ready.ready_handlers import ReadyStates, ask_start_conversation
from app.tgbot.handlers.ready.edit_handler import edit_profile, root_edit_profile
from app.tgbot.handlers.ready.start_search import start_conversation_new, cancel_queue


def register_ready(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_conversation_new,
        text='start_conversation',
        state=ReadyStates.ready)

    dp.register_callback_query_handler(
        edit_profile,
        text='edit_profile',
        state=ReadyStates.ready)

    dp.register_callback_query_handler(
        root_edit_profile,
        state=ReadyStates.edit_profile
    )

    dp.register_callback_query_handler(
        cancel_queue,
        text='cancel_queue',
        state=ReadyStates.add_to_queue
    )