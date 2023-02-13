from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.tgbot.utils.message_loader import messages

change_email_button = InlineKeyboardButton(text=messages['2.5'], callback_data='change_email')

wait_email_buttons = InlineKeyboardMarkup(row_width=1)
wait_email_buttons.add(change_email_button)

# registered_email_buttons = InlineKeyboardMarkup(row_width=1)
# registered_email_buttons.add(change_email_button)

retry_code_buttons = InlineKeyboardMarkup(row_width=1)
retry_code_buttons.add(InlineKeyboardButton(text=messages['2.11'], callback_data='retry'))
retry_code_buttons.add(change_email_button)