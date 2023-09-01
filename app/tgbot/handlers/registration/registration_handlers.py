from typing import List

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import User
from typeguard import check_type

from app.tgbot.handlers.ready.ready_handlers import ask_start_conversation
from app.tgbot.handlers.registration.registration_keyboard import (
    is_student_choice_buttons, get_interest_choice_markup, meeting_format_choice_buttons, \
    get_preferred_places_markup, info_buttons)
from app.tgbot.models.Criterion import CriterionBuilder, Interest, MeetingFormat, PreferredPlaces
from app.tgbot.models.Group import Group
from app.tgbot.models.MyUser import MyUserBuilder, MyUser, Role
from app.tgbot.models.WorkPlace import WorkPlace
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.Validate import Validate
from app.tgbot.utils.message_loader import messages
from app.tgbot.utils.state_access_wrapper import set_attr_to_state, get_attr_from_state


class RegistrationStates(StatesGroup):
    user_is_student_choice = State()
    user_info = State()
    user_info_typing = State()
    user_interest_choice = State()
    user_meeting_format_choice = State()
    user_preferred_places_choice = State()


logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)

# NOT A HANDLER
@logging_decorator
async def ask_is_student(message: types.Message):
    t_user_id = User.get_current().id
    await logger.print_info(f'user {t_user_id} went to ask is student stage')
    await RegistrationStates.user_is_student_choice.set()
    return await message.answer(messages['3.13'], reply_markup=is_student_choice_buttons)


@logging_decorator
async def read_is_student_choice(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext):
    user_builder: MyUserBuilder = MyUserBuilder.from_dict(await get_attr_from_state(state, 'user_builder'))
    check_type("user_builder", user_builder, MyUserBuilder)
    user_builder.set_role(Role.STUDENT if callback.data == 'is_student' else Role.WORKER)
    await set_attr_to_state(state, 'user_builder', user_builder.to_dict())
    bot: Bot = callback.bot
    t_user_id: int = User.get_current().id
    await bot.send_message(t_user_id, messages['3.13.6'].format(role="студент" if user_builder.role == Role.STUDENT else "сотрудник"))
    if (await bot_service.is_user_registered(t_user_id)) and not (await bot_service.is_old_user(t_user_id)):
        return await exit_registration(callback.bot, state, bot_service)
    else:
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
        return await message.answer(messages['3.11.1'], parse_mode="HTML")


@logging_decorator
async def read_info(message: types.Message, bot_service: BotService, state: FSMContext):
    t_user_id = User.get_current().id
    user_info: str = message.text.strip()
    msg = await Validate.take_reason_cancellation(user_info)
    if msg is not None:
        await message.answer(msg)
        return await message.answer(messages['3.15.10'])
    user_builder: MyUserBuilder = MyUserBuilder.from_dict(await get_attr_from_state(state, 'user_builder'))
    check_type("user_builder", user_builder, MyUserBuilder)
    user_builder.set_user_info(user_info)
    await set_attr_to_state(state, 'user_builder', user_builder.to_dict())
    if (await bot_service.is_user_registered(t_user_id)) and not (await bot_service.is_old_user(t_user_id)):
        return await exit_registration(message.bot, state, bot_service)
    else:
        return await ask_interests(message, bot_service, state)


@logging_decorator
async def keep_info(callback: types.CallbackQuery, state: FSMContext, bot_service: BotService):
    t_user_id = User.get_current().id
    if (await bot_service.is_user_registered(t_user_id)) and not (await bot_service.is_old_user(t_user_id)):
        return await exit_registration(callback.bot, state, bot_service)
    else:
        return await ask_interests(callback.message, bot_service, state)


@logging_decorator
async def change_info(callback: types.CallbackQuery):
    await RegistrationStates.user_info_typing.set()
    return await callback.message.answer(messages['3.11.2'], parse_mode="HTML")



#############################################################################
@logging_decorator
async def ask_interests(message: types.Message, bot_service: BotService, state: FSMContext):
    criterion_builder: CriterionBuilder = \
        CriterionBuilder.from_dict(await get_attr_from_state(state, 'criterion_builder'))
    assert criterion_builder is not None, "criterion_builder is NONE"
    await RegistrationStates.user_interest_choice.set()
    return await message.answer(messages['3.8.1'],
            reply_markup=get_interest_choice_markup(criterion_builder.interests))

@logging_decorator
async def interest_choice(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext):
    t_user_id = User.get_current().id
    criterion_builder: CriterionBuilder = \
        CriterionBuilder.from_dict(await get_attr_from_state(state, 'criterion_builder'))
    data = callback.data
    if data == "interest_further":
        if (await bot_service.is_user_registered(t_user_id)) and not (await bot_service.is_old_user(t_user_id)):
            return await exit_registration(callback.bot, state, bot_service)
        else:
            return await ask_meeting_format(callback.message, bot_service, state)
    else:
        assert data.startswith("skipp_")
        criterion_builder.xor_interests([Interest(data[6:])])
        await set_attr_to_state(state, 'criterion_builder', criterion_builder.to_dict())
        return await callback.message.edit_reply_markup(get_interest_choice_markup(criterion_builder.interests))

#############################################################################
@logging_decorator
async def ask_meeting_format(message: types.Message, bot_service: BotService, state: FSMContext):
    criterion_builder: CriterionBuilder = \
        CriterionBuilder.from_dict(await get_attr_from_state(state, 'criterion_builder'))
    assert criterion_builder is not None, "criterion_builder is NONE"
    await RegistrationStates.user_meeting_format_choice.set()
    return await message.answer(messages['3.14.1'],
                                reply_markup=meeting_format_choice_buttons)

@logging_decorator
async def meeting_format_choice(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext):
    criterion_builder: CriterionBuilder = \
        CriterionBuilder.from_dict(await get_attr_from_state(state, 'criterion_builder'))
    criterion_builder.set_meeting_format(MeetingFormat(callback.data))
    await set_attr_to_state(state, 'criterion_builder', criterion_builder.to_dict())
    if criterion_builder.meeting_format != MeetingFormat.ONLINE:
        return await ask_preferred_places(callback.message, bot_service, state)
    else:
        return await exit_registration(callback.message.bot, state, bot_service)

#################################################################################
@logging_decorator
async def ask_preferred_places(message: types.Message, bot_service: BotService, state: FSMContext):
    criterion_builder: CriterionBuilder = \
        CriterionBuilder.from_dict(await get_attr_from_state(state, 'criterion_builder'))
    assert criterion_builder is not None, "criterion_builder is NONE"
    await RegistrationStates.user_preferred_places_choice.set()
    return await message.answer(messages['3.15.1'],
                                reply_markup=get_preferred_places_markup(criterion_builder.preferred_places))

@logging_decorator
async def preferred_places_choice(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext):
    criterion_builder: CriterionBuilder = \
        CriterionBuilder.from_dict(await get_attr_from_state(state, 'criterion_builder'))
    data = callback.data
    if data == "interest_further":
        return await exit_registration(callback.message.bot, state, bot_service)
    else:
        assert data.startswith("skipp_")
        criterion_builder.xor_preferred_places([PreferredPlaces(data[6:])])
        await set_attr_to_state(state, 'criterion_builder', criterion_builder.to_dict())
        return await callback.message.edit_reply_markup(get_preferred_places_markup(criterion_builder.preferred_places))


# NOT A HANDLER;
@logging_decorator
async def exit_registration(bot: Bot, state: FSMContext, bot_service: BotService):
    user_builder: MyUserBuilder = MyUserBuilder.from_dict(await get_attr_from_state(state, 'user_builder'))
    criterion_builder: CriterionBuilder = \
        CriterionBuilder.from_dict(await get_attr_from_state(state, 'criterion_builder'))

    check_type("user_builder", user_builder, MyUserBuilder)
    check_type("criterion_builder", criterion_builder, CriterionBuilder)

    user_builder.set_old_user(False)
    my_user: MyUser = user_builder.to_user()

    await logger.print_info(f'user {my_user.t_user_id} upsert in database')
    await logger.print_info(f'criterion {my_user.t_user_id} upsert in database')
    await bot_service.upsert_user(user_builder.to_user())
    await bot_service.upsert_criterion(criterion_builder.to_criterion())

    message = messages['3.12']
    if criterion_builder.meeting_format != MeetingFormat.ONLINE:
        message += f" *Где встретимся*: {'; '.join(map(lambda preferred_place: preferred_place.value, criterion_builder.preferred_places))}"

    if my_user.role == Role.STUDENT:
        groups: List[Group] = await bot_service.get_grop_by_t_user_id(my_user.t_user_id)

        send_message = message.format(
            name=my_user.full_name,
            sex=my_user.sex.value,
            direction_name="Факультет",
            direction='; '.join(map(lambda group: group.faculty_name, groups)),
            info=my_user.user_info,
            interests=', '.join(map(lambda interest: interest.value, criterion_builder.interests)),
            meeting_format=criterion_builder.meeting_format.value)
    else:
        work_places: List[WorkPlace] = await bot_service.get_work_places_by_t_user_id(my_user.t_user_id)
        send_message = message.format(
            name=my_user.full_name,
            sex=my_user.sex.value,
            direction_name="Отдел",
            direction='; '.join(map(lambda work_place: work_place.name, work_places)),
            info=my_user.user_info,
            interests=', '.join(map(lambda interest: interest.value, criterion_builder.interests)),
            meeting_format=criterion_builder.meeting_format.value)

    await bot.send_message(my_user.t_user_id,
                               send_message,
                               parse_mode='Markdown')
    await logger.change_user_info(send_message)
    return await ask_start_conversation(bot)