from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.tgbot.models.Criterion import Criterion, MeetingFormat
from app.tgbot.models.MyUser import MyUser
from app.tgbot.utils.message_loader import messages

cancel_queue_buttons = InlineKeyboardMarkup()
cancel_queue_buttons.add(InlineKeyboardButton(text=messages['4.13'], callback_data='cancel_queue'))

edit_profile_buttons = InlineKeyboardMarkup()
edit_profile_buttons.add(InlineKeyboardButton(text=messages['4.2'], callback_data='edit_profile'))

start_conversation_buttons = InlineKeyboardMarkup()
start_conversation_buttons.add(InlineKeyboardButton(text=messages['4.2'], callback_data='edit_profile'))
start_conversation_buttons.add(InlineKeyboardButton(text=messages['4.3'], callback_data='start_conversation'))


def get_edit_profile_keyboard(my_user: MyUser, criterion: Criterion):
    settings = [(messages["4.6"], "info"), (messages["4.8"], "interests"),
                (messages["4.9"], "meeting_format")]
    if criterion.meeting_format != MeetingFormat.ONLINE:
        settings.append((messages["4.10"], "preferred_places"))
    if my_user.is_worker and my_user.is_student:
        settings.append((messages["4.7"], "role"))

    settings.append((messages["4.11"], "back"))

    markup = InlineKeyboardMarkup()
    for setting in settings:
        markup.add(InlineKeyboardButton(text=setting[0], callback_data=setting[1]))
    return markup
