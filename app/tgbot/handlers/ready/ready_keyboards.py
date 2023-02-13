from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.tgbot.utils.message_loader import messages

start_conversation_buttons = InlineKeyboardMarkup()
start_conversation_buttons.add(InlineKeyboardButton(text=messages['4.2'], callback_data='edit_profile'))
start_conversation_buttons.add(InlineKeyboardButton(text=messages['4.3'], callback_data='start_conversation'))