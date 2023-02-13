from aiogram import Dispatcher

from app.tgbot.handlers.start.start_handlers import start_chatting, StartStates, want_participate


def register_start(dp: Dispatcher):
    dp.register_message_handler(
        start_chatting,
        state=None)

    dp.register_callback_query_handler(
        want_participate,
        text=["want_participate"],
        state=StartStates.start)
