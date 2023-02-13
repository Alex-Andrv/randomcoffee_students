from aiogram import Dispatcher

from app.tgbot.handlers.user_have_not_username.user_have_not_username_handler import user_have_not_username_handler, \
    user_specified_username


def register_user_have_not_username(dp: Dispatcher):
    dp.register_message_handler(
        user_have_not_username_handler,
        state='*',
        is_user_have_username=False)

    dp.register_callback_query_handler(
        user_have_not_username_handler,
        state='*',
        is_user_have_username=False)

    dp.register_callback_query_handler(
        user_specified_username,
        text='recheck_availability_username',
        state='*',
        is_user_have_username=True
    )