from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.tgbot.utils.message_loader import messages

start_approve_button = InlineKeyboardMarkup()
start_approve_button.add(InlineKeyboardButton(text=messages['6.3'], callback_data='confirm'))