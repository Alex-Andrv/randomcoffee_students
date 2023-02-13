import re

from aiogram import Dispatcher

from app.tgbot.handlers.email.email_handlers import read_email, EmailStates, read_code, \
    read_invalid_code, retry_code, change_email

code_regex = re.compile(r'[\d]{6}')

def register_email(dp: Dispatcher):

    dp.register_message_handler(
        read_email,
        state=EmailStates.reading_email)

    dp.register_message_handler(
        read_code,
        lambda msg: re.fullmatch(code_regex, msg.text),
        state=EmailStates.awaiting_code)

    dp.register_message_handler(
        read_invalid_code,
        state=EmailStates.awaiting_code)

    dp.register_callback_query_handler(
        retry_code,
        text='proceed',
        state=EmailStates.reading_email)

    dp.register_callback_query_handler(
        retry_code,
        text='retry',
        state=EmailStates.wrong_code)

    dp.register_callback_query_handler(
        retry_code,
        text='retry',
        state=EmailStates.awaiting_code)

    dp.register_callback_query_handler(
        change_email,
        text='change_email',
        state=EmailStates.awaiting_code)

    dp.register_callback_query_handler(
        change_email,
        text='change_email',
        state=EmailStates.wrong_code)
