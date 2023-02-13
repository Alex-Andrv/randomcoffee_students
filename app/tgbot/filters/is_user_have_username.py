from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsUsernameMissingFilter(BoundFilter):
    key = 'is_user_have_username'

    def __init__(self, is_user_have_username):
        self.is_user_have_username = is_user_have_username

    async def check(self, message: types.Message | types.CallbackQuery):
        user_name = message.from_user.username
        is_not_empty_name: bool = user_name is not None and len(user_name) != 0
        return is_not_empty_name == self.is_user_have_username
