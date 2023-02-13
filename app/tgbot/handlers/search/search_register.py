from aiogram import Dispatcher

from app.tgbot.handlers.search.search_hendlers import SearchStates, search_search, cancel_search


def register_search(dp: Dispatcher):
    dp.register_callback_query_handler(
        search_search,
        state=SearchStates.search_format_choice)

    dp.register_callback_query_handler(
        cancel_search,
        state=SearchStates.wait_companion,
        text="cancel_search")
