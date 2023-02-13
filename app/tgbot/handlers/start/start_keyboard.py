from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.tgbot.utils.message_loader import messages

start_chatting_button = InlineKeyboardMarkup(row_width=1)
start_chatting_button.add(InlineKeyboardButton(messages['1.2'], callback_data='want_participate'))