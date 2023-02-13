from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.tgbot.utils.message_loader import messages

search_format_choice_buttons = InlineKeyboardMarkup(row_width=1)
search_format_choice_buttons.add(InlineKeyboardButton(text=messages['5.0.1'], callback_data=messages['5.0.1']))
search_format_choice_buttons.add(InlineKeyboardButton(text=messages['5.0.2'], callback_data=messages['5.0.2']))
search_format_choice_buttons.add(InlineKeyboardButton(text=messages['5.0.3'], callback_data=messages['5.0.3']))
search_format_choice_buttons.add(InlineKeyboardButton(text=messages['5.0.4'], callback_data=messages['5.0.4']))

wait_companion_button = InlineKeyboardMarkup()
wait_companion_button.add(InlineKeyboardButton(text=messages['5.3'], callback_data='cancel_search'))