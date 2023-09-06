from aiogram import Dispatcher

from app.tgbot.handlers.ready.ready_handlers import ReadyStates
from app.tgbot.handlers.ready.edit_handler import root_edit_profile, cancel_queue_and_edit_profile


def register_ready(dp: Dispatcher):
    dp.register_callback_query_handler(
        cancel_queue_and_edit_profile,
        text='edit_profile',
        state=ReadyStates.add_to_queue)

    dp.register_callback_query_handler(
        cancel_queue_and_edit_profile,
        text='cancel_queue',
        state=ReadyStates.add_to_queue)

    dp.register_callback_query_handler(
        root_edit_profile,
        state=ReadyStates.edit_profile
    )