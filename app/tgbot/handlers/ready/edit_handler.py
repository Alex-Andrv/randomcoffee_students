from datetime import datetime, timedelta

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import User

from app.tgbot.exseptions.exseptions import NotFoundInEdit
from app.tgbot.handlers.ready.ready_keyboards import get_edit_profile_keyboard
from app.tgbot.handlers.ready.ready_start_conversation import start_conversation_new
from app.tgbot.handlers.ready.ready_state import ReadyStates
from app.tgbot.handlers.registration.registration_handlers import ask_for_info, ask_interests, ask_meeting_format, \
    ask_preferred_places, ask_is_student
from app.tgbot.models import MyUser
from app.tgbot.models.Criterion import Criterion, CriterionBuilder
from app.tgbot.models.MyUser import MyUserBuilder
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import logging_decorator_factory, BotLogger
from app.tgbot.utils.state_access_wrapper import set_attr_to_state
from app.tgbot.utils.message_loader import messages

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


@logging_decorator
async def edit_profile(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext):
    t_user_id: int = callback.from_user.id
    await logger.print_info(f'user {t_user_id} is editing profile')
    # TODO initialize user_builder
    my_user: MyUser = await bot_service.get_user_by_t_user_id(t_user_id)
    await set_attr_to_state(state, 'user_builder', MyUserBuilder.from_user(my_user).to_dict())
    criterion: Criterion = await bot_service.get_criterion_by_t_user_id(t_user_id)
    await set_attr_to_state(state, 'criterion_builder', CriterionBuilder.from_criterion(criterion).to_dict())

    await ReadyStates.edit_profile.set()
    return await callback.message.answer(messages["4.5"], reply_markup=get_edit_profile_keyboard(my_user, criterion))


@logging_decorator
async def root_edit_profile(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext):
    data = callback.data
    if data == "info":
        return await ask_for_info(callback.message, bot_service)
    elif data == "interests":
        return await ask_interests(callback.message, bot_service, state)
    elif data == "meeting_format":
        return await ask_meeting_format(callback.message, bot_service, state)
    elif data == "preferred_places":
        return await ask_preferred_places(callback.message, bot_service, state)
    elif data == "role":
        return await ask_is_student(callback.message)
    elif data == "back":
        return await start_conversation_new(callback.message.bot, bot_service)
    raise NotFoundInEdit()


def timestamp_to_week_day(timestamp: datetime):
    # Используем функцию weekday() для получения номера дня недели (понедельник = 0, воскресенье = 6)
    weekday_num = timestamp.weekday()
    day_name = ["понедельник", "вторник", "среду", "четверг", "пятницу", "субботу", "воскресенье"]
    # Используем список calendar.day_name для получения названия дня недели на основе номера
    return day_name[weekday_num]


@logging_decorator
async def cancel_queue_and_edit_profile(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext):
    t_user_id = User.get_current().id
    message = callback.message
    matching_time: datetime = await bot_service.get_matching_time_by_t_user_id(t_user_id)
    now: datetime = datetime.now()
    await logger.print_info("try delete user from queue")
    if matching_time - now < timedelta(minutes=130):
        await logger.print_info("can't delete from queue")
        return await message.answer(
            messages['4.15'])
    else:
        await logger.print_info("seduced delete from queue")
        await bot_service.delete_user_from_queue(t_user_id)
        await message.answer(messages['4.14'])
        return await edit_profile(callback, bot_service, state)