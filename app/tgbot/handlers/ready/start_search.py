from aiogram import types

from app.tgbot.handlers.search.search_hendlers import search_format_choice_search
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


@logging_decorator
async def start_conversation(callback: types.CallbackQuery):
    return await search_format_choice_search(callback)