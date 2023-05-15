import re

from aiogram import Dispatcher

from app.tgbot.handlers.email.email_handlers import read_email, EmailStates, read_code, \
    read_invalid_code, retry_code, change_email
from app.tgbot.handlers.itmoId.itmoid_handlers import ItmoIdStates, validate_oauth

code_regex = re.compile(r'[\d]{6}')

def register_itmoid(dp: Dispatcher):

    dp.register_callback_query_handler(
        validate_oauth,
        text='check_registrate',
        state=ItmoIdStates.OAuth_start)
