from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.tgbot.utils.message_loader import messages

recheck_username_button = InlineKeyboardMarkup(row_width=1)
recheck_username_button.add(InlineKeyboardButton(messages['8.2'], callback_data='recheck_availability_username'))