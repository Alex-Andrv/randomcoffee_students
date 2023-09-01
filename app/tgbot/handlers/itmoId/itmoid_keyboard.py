from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, LoginUrl

from app.tgbot.utils.message_loader import messages


def get_itmoid_keyboard(user_id):
    offer_oauth_registrate_button = InlineKeyboardButton(
        text=messages['21.3'], callback_data='oauth_registrate',
        url=f'https://id.itmo.ru/auth/realms/itmo/protocol/openid-connect/auth?client_id=itmoffe-bot&response_type=code&scope=openid profile email edu work&redirect_uri=https://rcoffeestudent.itmo.ru&state={user_id}')
    check_registrate_button = InlineKeyboardButton(text=messages['21.2'], callback_data='check_registrate')
    oauth_buttons = InlineKeyboardMarkup(row_width=2)
    oauth_buttons.add(offer_oauth_registrate_button, check_registrate_button)
    return oauth_buttons