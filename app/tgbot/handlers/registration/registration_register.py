from aiogram import Dispatcher

from app.tgbot.handlers.registration.registration_handlers import read_info, RegistrationStates, ask_for_info, \
    ask_is_student, read_is_student_choice, ask_interests, interest_choice, ask_meeting_format, meeting_format_choice, \
    ask_preferred_places, preferred_places_choice, keep_info, change_info


def register_registration(dp: Dispatcher):
    dp.register_callback_query_handler(
        read_is_student_choice,
        state=RegistrationStates.user_is_student_choice)

    dp.register_message_handler(
        read_info,
        state=RegistrationStates.user_info_typing)

    dp.register_callback_query_handler(
        interest_choice,
        state=RegistrationStates.user_interest_choice)

    dp.register_callback_query_handler(
        meeting_format_choice,
        state=RegistrationStates.user_meeting_format_choice)

    dp.register_callback_query_handler(
        preferred_places_choice,
        state=RegistrationStates.user_preferred_places_choice)

    dp.register_callback_query_handler(
        keep_info,
        text='keep_info',
        state=RegistrationStates.user_info)

    dp.register_callback_query_handler(
        change_info,
        text='change_info',
        state=RegistrationStates.user_info)
