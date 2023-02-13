from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import User
from typeguard import check_type

from app.tgbot.handlers.ready.ready_handlers import ask_start_conversation
from app.tgbot.handlers.registration.registration_keyboard import name_buttons, had_direction_buttons, \
    direction_choice_buttons, info_buttons, had_course_buttons, course_choice_buttons, had_sex_buttons, \
    sex_choice_buttons
from app.tgbot.models.MyUser import MyUserBuilder, MyUser, Direction, Sex, Course
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.Validate import Validate
from app.tgbot.utils.message_loader import messages
from app.tgbot.utils.state_access_wrapper import set_attr_to_state, get_attr_from_state


class RegistrationStates(StatesGroup):
    full_name = State()
    set_full_name = State()
    user_sex = State()
    user_sex_choice = State()
    user_direction = State()
    user_direction_choice = State()
    user_course = State()
    user_course_choice = State()
    user_info = State()
    user_info_typing = State()


logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


# NOT A HANDLER;
@logging_decorator
async def ask_for_name(message: types.Message, bot_service: BotService, state: FSMContext):
    t_user_id = User.get_current().id
    my_user: MyUser = await bot_service.get_user_by_t_user_id(t_user_id)
    if my_user:
        await set_attr_to_state(state, 'user_builder', MyUserBuilder.from_user(my_user).to_dict())
        await RegistrationStates.full_name.set()
        return await message.answer(messages['3.1.2'].format(name=my_user.full_name),
                                    reply_markup=name_buttons)
    else:
        await RegistrationStates.set_full_name.set()
        return await message.answer(messages['3.1.1'])


@logging_decorator
async def set_full_name(message: types.Message, bot_service: BotService, state: FSMContext):
    full_name: str = message.text.strip()
    if not Validate.validate_full_name(full_name):
        await message.answer(messages['3.1.1.1'])
        return await ask_for_name(messages, bot_service, state)
    user_builder: MyUserBuilder = MyUserBuilder.from_dict(await get_attr_from_state(state, 'user_builder'))
    check_type("user_builder", user_builder, MyUserBuilder)
    user_builder.set_full_name(full_name)
    await set_attr_to_state(state, 'user_builder', user_builder.to_dict())
    await logger.print_info(f'user: {User.get_current().id} set/change full name')
    await set_attr_to_state(state, 'user_builder', user_builder.to_dict())
    await message.answer(messages['3.2.3.0'].format(full_name=full_name))
    return await ask_for_sex(message, bot_service)


@logging_decorator
async def keep_full_name(callback: types.CallbackQuery, bot_service: BotService):
    return await ask_for_sex(callback.message, bot_service)


@logging_decorator
async def change_full_name(callback: types.CallbackQuery):
    await RegistrationStates.set_full_name.set()
    return await callback.message.answer(messages['3.2.2'])


# NOT A HANDLER;
@logging_decorator
async def ask_for_sex(message: types.Message, bot_service: BotService):
    t_user_id = User.get_current().id
    my_user: MyUser = await bot_service.get_user_by_t_user_id(t_user_id)
    await logger.print_info(f'user {t_user_id} went to direction stage')
    if my_user:
        await RegistrationStates.user_sex.set()
        return await message.answer(messages['3.2.3.4'].format(sex=my_user.sex.value),
                                    reply_markup=had_sex_buttons)
    else:
        return await show_sex_choices(message)


@logging_decorator
async def show_sex_choices(message: types.Message):
    await RegistrationStates.user_sex_choice.set()
    return await message.answer(messages['3.2.3.1'],
                                reply_markup=sex_choice_buttons,
                                parse_mode='Markdown')


@logging_decorator
async def change_sex(callback: types.CallbackQuery):
    return await show_sex_choices(callback.message)


@logging_decorator
async def keep_sex(callback: types.CallbackQuery, bot_service: BotService):
    return await ask_for_direction(callback.message, bot_service)


@logging_decorator
async def read_sex_choice(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext):
    user_builder: MyUserBuilder = MyUserBuilder.from_dict(await get_attr_from_state(state, 'user_builder'))
    check_type("user_builder", user_builder, MyUserBuilder)
    sex: Sex = Sex(callback.data)
    user_builder.set_sex(sex)
    await set_attr_to_state(state, 'user_builder', user_builder.to_dict())
    bot: Bot = callback.bot
    user_id: int = User.get_current().id
    await bot.send_message(user_id, messages['3.2.3.6.0'].format(sex=sex.value))
    return await ask_for_direction(callback.message, bot_service)


# NOT A HANDLER;
@logging_decorator
async def ask_for_direction(message: types.Message, bot_service: BotService):
    t_user_id = User.get_current().id
    my_user: MyUser = await bot_service.get_user_by_t_user_id(t_user_id)
    await logger.print_info(f'user {t_user_id} went to direction stage')
    if my_user:
        await RegistrationStates.user_direction.set()
        return await message.answer(messages['3.3.2'].format(direction=my_user.direction.value),
                                    reply_markup=had_direction_buttons)
    else:
        return await show_direction_choices(message)


@logging_decorator
async def show_direction_choices(message: types.Message):
    await RegistrationStates.user_direction_choice.set()
    return await message.answer(messages['3.3.1'],
                                reply_markup=direction_choice_buttons,
                                parse_mode='Markdown')


@logging_decorator
async def change_direction(callback: types.CallbackQuery):
    return await show_direction_choices(callback.message)


@logging_decorator
async def keep_direction(callback: types.CallbackQuery, bot_service: BotService):
    return await ask_for_course(callback.message, bot_service)


@logging_decorator
async def read_direction_choice(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext):
    user_builder: MyUserBuilder = MyUserBuilder.from_dict(await get_attr_from_state(state, 'user_builder'))
    check_type("user_builder", user_builder, MyUserBuilder)
    direction: Direction = Direction(callback.data)
    user_builder.set_direction(direction)
    await set_attr_to_state(state, 'user_builder', user_builder.to_dict())
    bot: Bot = callback.bot
    user_id: int = User.get_current().id
    await bot.send_message(user_id, messages['3.6.1.0'].format(direction=direction.value))
    return await ask_for_course(callback.message, bot_service)


# NOT A HANDLER;
@logging_decorator
async def ask_for_course(message: types.Message, bot_service: BotService):
    t_user_id = User.get_current().id
    my_user: MyUser = await bot_service.get_user_by_t_user_id(t_user_id)
    await logger.print_info(f'user {t_user_id} went to course stage')
    if my_user:
        await RegistrationStates.user_course.set()
        return await message.answer(messages['3.7.2'].format(course=my_user.course.value),
                                    reply_markup=had_course_buttons)
    else:
        return await show_course_choice(message)


@logging_decorator
async def show_course_choice(message: types.Message):
    await RegistrationStates.user_course_choice.set()
    return await message.answer(messages['3.7.1'],
                                reply_markup=course_choice_buttons,
                                parse_mode='Markdown')


@logging_decorator
async def change_course(callback: types.CallbackQuery):
    return await show_course_choice(callback.message)


@logging_decorator
async def keep_course(callback: types.CallbackQuery, bot_service: BotService):
    return await ask_for_info(callback.message, bot_service)


@logging_decorator
async def read_course_choice(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext):
    user_builder: MyUserBuilder = MyUserBuilder.from_dict(await get_attr_from_state(state, 'user_builder'))
    check_type("user_builder", user_builder, MyUserBuilder)
    course: Course = Course(callback.data)
    user_builder.set_course(course)
    await set_attr_to_state(state, 'user_builder', user_builder.to_dict())
    bot: Bot = callback.bot
    user_id: int = User.get_current().id
    await bot.send_message(user_id, messages['3.7.5.0'].format(course=course.value))
    return await ask_for_info(callback.message, bot_service)


# NOT A HANDLER;
@logging_decorator
async def ask_for_info(message: types.Message, bot_service: BotService):
    t_user_id = User.get_current().id
    my_user: MyUser = await bot_service.get_user_by_t_user_id(t_user_id)
    await logger.print_info(f'user {t_user_id} went to personal info stage')
    if my_user:
        await RegistrationStates.user_info.set()
        return await message.answer(messages['3.9'].format(info=my_user.user_info),
                                    reply_markup=info_buttons)
    else:
        await RegistrationStates.user_info_typing.set()
        return await message.answer(messages['3.11.1'])


@logging_decorator
async def read_info(message: types.Message, bot_service: BotService, state: FSMContext):
    user_info: str = message.text.strip()
    if not Validate.validate_user_info(user_info):
        await message.answer(messages['3.11.1.1'])
        return await ask_for_info(message, bot_service)
    user_builder: MyUserBuilder = MyUserBuilder.from_dict(await get_attr_from_state(state, 'user_builder'))
    check_type("user_builder", user_builder, MyUserBuilder)
    user_builder.set_user_info(user_info)
    await set_attr_to_state(state, 'user_builder', user_builder.to_dict())
    return await exit_registration(message.bot, state, bot_service)


@logging_decorator
async def keep_info(callback: types.CallbackQuery, state: FSMContext, bot_service: BotService):
    return await exit_registration(callback.bot, state, bot_service)


@logging_decorator
async def change_info(callback: types.CallbackQuery):
    await RegistrationStates.user_info_typing.set()
    return await callback.message.answer(messages['3.11.2'])


# NOT A HANDLER;
@logging_decorator
async def exit_registration(bot: Bot, state: FSMContext, bot_service: BotService):
    user_builder: MyUserBuilder = MyUserBuilder.from_dict(await get_attr_from_state(state, 'user_builder'))
    check_type("user_builder", user_builder, MyUserBuilder)
    user_builder.set_user_name(User.get_current().username)

    my_user: MyUser = user_builder.to_user()

    await logger.print_info(f'user {my_user.t_user_id} upsert in database')
    await bot_service.upsert_user(my_user)

    await bot.send_message(my_user.t_user_id,
                           messages['3.12'].format(
                               name=my_user.full_name,
                               sex=my_user.sex.value,
                               direction=my_user.direction.value,
                               course=my_user.course.value,
                               info=my_user.user_info),
                           parse_mode='Markdown')
    return await ask_start_conversation(bot)
