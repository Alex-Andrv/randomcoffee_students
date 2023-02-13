from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.tgbot.utils.message_loader import messages

name_buttons = InlineKeyboardMarkup(row_width=1)
name_buttons.add(InlineKeyboardButton(text=messages['3.2.3'], callback_data='keep_name'))
name_buttons.add(InlineKeyboardButton(text=messages['3.2.1'], callback_data='change_name'))


had_sex_buttons = InlineKeyboardMarkup(row_width=1)
had_sex_buttons.add(InlineKeyboardButton(text=messages['3.2.3.6'], callback_data='keep_sex'))
had_sex_buttons.add(InlineKeyboardButton(text=messages['3.2.3.5'], callback_data='change_sex'))

sex_choice_buttons = InlineKeyboardMarkup(row_width=1)
sex_choice_buttons.add(InlineKeyboardButton(text=messages['3.2.3.2'], callback_data=messages['3.2.3.2']))
sex_choice_buttons.add(InlineKeyboardButton(text=messages['3.2.3.3'], callback_data=messages['3.2.3.3']))


had_direction_buttons = InlineKeyboardMarkup(row_width=1)
had_direction_buttons.add(InlineKeyboardButton(text=messages['3.6'], callback_data='keep_direction'))
had_direction_buttons.add(InlineKeyboardButton(text=messages['3.6.1'], callback_data='change_direction'))

direction_choice_buttons = InlineKeyboardMarkup(row_width=1)
direction_choice_buttons.add(InlineKeyboardButton(text=messages['3.4.1'], callback_data=messages['3.4.1']))
direction_choice_buttons.add(InlineKeyboardButton(text=messages['3.4.2'], callback_data=messages['3.4.2']))
direction_choice_buttons.add(InlineKeyboardButton(text=messages['3.4.3'], callback_data=messages['3.4.3']))
direction_choice_buttons.add(InlineKeyboardButton(text=messages['3.4.4'], callback_data=messages['3.4.4']))
direction_choice_buttons.add(InlineKeyboardButton(text=messages['3.4.5'], callback_data=messages['3.4.5']))
direction_choice_buttons.add(InlineKeyboardButton(text=messages['3.4.6'], callback_data=messages['3.4.6']))
direction_choice_buttons.add(InlineKeyboardButton(text=messages['3.4.7'], callback_data=messages['3.4.7']))
direction_choice_buttons.add(InlineKeyboardButton(text=messages['3.4.8'], callback_data=messages['3.4.8']))
direction_choice_buttons.add(InlineKeyboardButton(text=messages['3.4.9'], callback_data=messages['3.4.9']))
direction_choice_buttons.add(InlineKeyboardButton(text=messages['3.4.10'], callback_data=messages['3.4.10']))

course_choice_buttons = InlineKeyboardMarkup(row_width=1)
course_choice_buttons.add(InlineKeyboardButton(text=messages['3.7.3.1'], callback_data=messages['3.7.3.1']))
course_choice_buttons.add(InlineKeyboardButton(text=messages['3.7.3.2'], callback_data=messages['3.7.3.2']))
course_choice_buttons.add(InlineKeyboardButton(text=messages['3.7.3.3'], callback_data=messages['3.7.3.3']))
course_choice_buttons.add(InlineKeyboardButton(text=messages['3.7.3.4'], callback_data=messages['3.7.3.4']))
course_choice_buttons.add(InlineKeyboardButton(text=messages['3.7.3.5'], callback_data=messages['3.7.3.5']))
course_choice_buttons.add(InlineKeyboardButton(text=messages['3.7.3.6'], callback_data=messages['3.7.3.6']))
course_choice_buttons.add(InlineKeyboardButton(text=messages['3.7.3.7'], callback_data=messages['3.7.3.7']))

had_course_buttons = InlineKeyboardMarkup(row_width=1)
had_course_buttons.add(InlineKeyboardButton(text=messages['3.7.4'], callback_data='keep_course'))
had_course_buttons.add(InlineKeyboardButton(text=messages['3.7.5'], callback_data='change_course'))

interest_choice_buttons = InlineKeyboardMarkup(row_width=1)
interest_choice_buttons.add(InlineKeyboardButton(text=messages['3.8.2.1'], callback_data=messages['3.8.2.1']))
interest_choice_buttons.add(InlineKeyboardButton(text=messages['3.8.2.2'], callback_data=messages['3.8.2.2']))
interest_choice_buttons.add(InlineKeyboardButton(text=messages['3.8.2.3'], callback_data=messages['3.8.2.3']))
interest_choice_buttons.add(InlineKeyboardButton(text=messages['3.8.2.4'], callback_data=messages['3.8.2.4']))
interest_choice_buttons.add(InlineKeyboardButton(text=messages['3.8.2.5'], callback_data=messages['3.8.2.5']))
interest_choice_buttons.add(InlineKeyboardButton(text=messages['3.8.2.6'], callback_data=messages['3.8.2.6']))
interest_choice_buttons.add(InlineKeyboardButton(text=messages['3.8.2.7'], callback_data=messages['3.8.2.7']))
interest_choice_buttons.add(InlineKeyboardButton(text=messages['3.8.2.8'], callback_data=messages['3.8.2.8']))
interest_choice_buttons.add(InlineKeyboardButton(text=messages['3.8.2.9'], callback_data=messages['3.8.2.9']))
interest_choice_buttons.add(InlineKeyboardButton(text=messages['3.8.2.10'], callback_data=messages['3.8.2.10']))

had_interest_buttons = InlineKeyboardMarkup(row_width=1)
had_interest_buttons.add(InlineKeyboardButton(text=messages['3.8.4'], callback_data='keep_interest'))
had_interest_buttons.add(InlineKeyboardButton(text=messages['3.8.5'], callback_data='change_interest'))

info_buttons = InlineKeyboardMarkup(row_width=1)
info_buttons.add(InlineKeyboardButton(text=messages['3.10.2'], callback_data='keep_info'))
info_buttons.add(InlineKeyboardButton(text=messages['3.10.1'], callback_data='change_info'))
