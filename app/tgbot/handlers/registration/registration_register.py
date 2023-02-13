from aiogram import Dispatcher

from app.tgbot.handlers.registration.registration_handlers import set_full_name, RegistrationStates, read_info, \
    keep_full_name, change_full_name, keep_info, change_info, keep_direction, change_direction, \
    read_direction_choice, keep_course, change_course, read_course_choice, change_sex, keep_sex, read_sex_choice


def register_registration(dp: Dispatcher):
    dp.register_message_handler(
        set_full_name,
        state=RegistrationStates.set_full_name)

    dp.register_callback_query_handler(
        keep_full_name,
        text='keep_name',
        state=RegistrationStates.full_name)

    dp.register_callback_query_handler(
        change_full_name,
        text='change_name',
        state=RegistrationStates.full_name)

    dp.register_callback_query_handler(
        keep_sex,
        text='keep_sex',
        state=RegistrationStates.user_sex)

    dp.register_callback_query_handler(
        change_sex,
        text='change_sex',
        state=RegistrationStates.user_sex)

    dp.register_callback_query_handler(
        read_sex_choice,
        state=RegistrationStates.user_sex_choice)

    dp.register_callback_query_handler(
        keep_direction,
        text='keep_direction',
        state=RegistrationStates.user_direction)

    dp.register_callback_query_handler(
        change_direction,
        text='change_direction',
        state=RegistrationStates.user_direction)

    dp.register_callback_query_handler(
        read_direction_choice,
        state=RegistrationStates.user_direction_choice)

    dp.register_callback_query_handler(
        keep_course,
        text='keep_course',
        state=RegistrationStates.user_course)

    dp.register_callback_query_handler(
        change_course,
        text='change_course',
        state=RegistrationStates.user_course)

    dp.register_callback_query_handler(
        read_course_choice,
        state=RegistrationStates.user_course_choice)

    dp.register_message_handler(
        read_info,
        state=RegistrationStates.user_info_typing)

    dp.register_callback_query_handler(
        keep_info,
        text='keep_info',
        state=RegistrationStates.user_info)

    dp.register_callback_query_handler(
        change_info,
        text='change_info',
        state=RegistrationStates.user_info)
