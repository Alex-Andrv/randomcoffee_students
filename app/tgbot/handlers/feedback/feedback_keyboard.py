from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.tgbot.utils.message_loader import messages

feedback_button = InlineKeyboardMarkup(row_width=1)
feedback_button.add(InlineKeyboardButton(text=messages['7.2'], callback_data='feedback'))

met_button = InlineKeyboardButton(text=messages['7.5'], callback_data='confirm')
didnt_meet_button = InlineKeyboardButton(text=messages['7.7'], callback_data='didnt_meet')

feedback_forced_buttons = InlineKeyboardMarkup(row_width=1)
feedback_forced_buttons.add(met_button)
feedback_forced_buttons.add(didnt_meet_button)

feedback_loose_buttons = InlineKeyboardMarkup(row_width=1)
feedback_loose_buttons.add(met_button)
feedback_loose_buttons.add(InlineKeyboardButton(text=messages['7.6'], callback_data='unknown'))
feedback_loose_buttons.add(didnt_meet_button)

feedback_like_buttons = InlineKeyboardMarkup(row_width=1)
feedback_like_buttons.add(InlineKeyboardButton(text=messages['7.9.1'], callback_data='5_hearts'))
feedback_like_buttons.add(InlineKeyboardButton(text=messages['7.9.2'], callback_data='4_hearts'))
feedback_like_buttons.add(InlineKeyboardButton(text=messages['7.9.3'], callback_data='3_hearts'))
feedback_like_buttons.add(InlineKeyboardButton(text=messages['7.9.4'], callback_data='2_hearts'))
feedback_like_buttons.add(InlineKeyboardButton(text=messages['7.9.5'], callback_data='1_hearts'))

feedback_problem_buttons = InlineKeyboardMarkup(row_width=1)
feedback_problem_buttons.add(InlineKeyboardButton(text=messages['7.17'], callback_data='no_reply'))
feedback_problem_buttons.add(InlineKeyboardButton(text=messages['7.18'], callback_data='time_problem'))
feedback_problem_buttons.add(InlineKeyboardButton(text=messages['7.19'], callback_data='other_problem'))
feedback_problem_buttons.add(InlineKeyboardButton(text=messages['7.20'], callback_data='bot_problem'))