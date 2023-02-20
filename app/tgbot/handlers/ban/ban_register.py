from aiogram import Dispatcher

from app.tgbot.handlers.ban.ban_handler import user_ban_handler, BanStates


def register_user_ban(dp: Dispatcher):
    dp.register_message_handler(
        user_ban_handler,
        state=BanStates.ban_state)

    dp.register_callback_query_handler(
        user_ban_handler,
        state=BanStates.ban_state)