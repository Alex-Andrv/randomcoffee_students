from aiogram import Dispatcher, types

from app.tgbot.handlers.suggestions_button.suggestions_handlers import send_suggestion,\
    read_suggestion, SuggestionStates


def register_suggestion_button(dp: Dispatcher):
    dp.register_message_handler(
        read_suggestion,
        state=SuggestionStates.reading_suggestion, is_user_have_username=True)

    dp.register_message_handler(
        send_suggestion,
        commands=["suggestion"],
        state='*', is_user_have_username=True)
