from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.tgbot.models.Criterion import Interest, PreferredPlaces
from app.tgbot.utils.message_loader import messages

sex_choice_buttons = InlineKeyboardMarkup(row_width=1)
sex_choice_buttons.add(InlineKeyboardButton(text=messages['3.2.3.2'], callback_data=messages['3.2.3.2']))
sex_choice_buttons.add(InlineKeyboardButton(text=messages['3.2.3.3'], callback_data=messages['3.2.3.3']))


def get_interactive_choice_markup(selected_choice: set, choices: list):
    interactive_choice_buttons = InlineKeyboardMarkup(row_width=1)
    selected = '✅'
    choices = list(
        map(lambda choice: (selected + choice if choice in selected_choice else choice, choice) , choices))
    [interactive_choice_buttons.add(InlineKeyboardButton(text=choice, callback_data=f"skipp_{choice_calldata}"))
     for choice, choice_calldata in
     choices]
    return interactive_choice_buttons


def get_interest_choice_markup(selected_interests: set[Interest]):
    interests = [messages[f'3.8.2.{i}'] for i in range(1, 10)]
    markup = get_interactive_choice_markup(selected_interests, interests)
    markup.add(InlineKeyboardButton(text=messages[f'3.8.2.10'], callback_data="interest_further"))
    return markup


def get_preferred_places_markup(selected_preferred_places: set[PreferredPlaces]):
    preferred_places = [messages[f'3.15.{i}'] for i in range(2, 9)]
    markup = get_interactive_choice_markup(selected_preferred_places, preferred_places)
    markup.add(InlineKeyboardButton(text=messages[f'3.15.9'], callback_data="interest_further"))
    return markup


is_student_choice_buttons = InlineKeyboardMarkup(row_width=1)
is_student_choice_buttons.add(InlineKeyboardButton(text=messages['3.13.1'], callback_data='is_student'))
is_student_choice_buttons.add(InlineKeyboardButton(text=messages['3.13.2'], callback_data='is_worker'))

meeting_format_choice_buttons = InlineKeyboardMarkup(row_width=1)
meeting_format_choice_buttons.add(InlineKeyboardButton(text=messages['3.14.2'], callback_data=messages['3.14.2']))
meeting_format_choice_buttons.add(InlineKeyboardButton(text=messages['3.14.3'], callback_data=messages['3.14.3']))
meeting_format_choice_buttons.add(InlineKeyboardButton(text=messages['3.14.4'], callback_data=messages['3.14.4']))


info_buttons = InlineKeyboardMarkup(row_width=1)
info_buttons.add(InlineKeyboardButton(text=messages['3.10.2'], callback_data='keep_info'))
info_buttons.add(InlineKeyboardButton(text=messages['3.10.1'], callback_data='change_info'))
