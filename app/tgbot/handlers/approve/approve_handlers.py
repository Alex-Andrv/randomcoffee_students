import typing

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types.base import Integer

from app.tgbot.handlers.approve.approve_keyboard import start_approve_button
from app.tgbot.handlers.feedback.feedback_handlers import feedback_start
from app.tgbot.middlewares.RemovePreviousButtons import delete_button_on_previous_message, \
    save_sending_message_attribute
from app.tgbot.models.MyUser import MyUser
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.message_loader import messages


class ApproveStates(StatesGroup):
    approve = State()


logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


# NOT A HANDLER;
@logging_decorator
async def ping_user(t_user_id: Integer, companion_id: Integer, bot: Bot, bot_service: BotService):
    companion: MyUser = await bot_service.get_user_by_t_user_id(companion_id)
    await bot.send_message(
        t_user_id,
        messages['6.1'].format(
            full_name=companion.full_name,
            sex=companion.sex.value,
            direction=companion.direction.value,
            course=companion.course.value,
            info=companion.user_info,
            user_name=companion.user_name),
        parse_mode='Markdown')
    return await bot.send_message(
        t_user_id,
        messages['6.2'],
        reply_markup=start_approve_button)


# NOT A HANDLER;
@logging_decorator
async def start_approve(
        callback: types.CallbackQuery,
        companion_id: Integer,
        bot_service: BotService,
        state: FSMContext):

    old_state: typing.Optional[str] = await state.storage.get_state(user=companion_id)
    if old_state != 'SearchStates:wait_companion':
        await logger.print_error(f"user ({companion_id}) not in SearchStates:wait_companion state")

    await ApproveStates.approve.set()
    await state.storage.set_state(user=companion_id, state='ApproveStates:approve')

    t_user_id: Integer = callback.from_user.id

    await logger.print_info(f'user {t_user_id} found companion {companion_id}')

    bot: Bot = callback.bot

    await logger.print_info(f'send message to companion={companion_id}')
    companion_message = await ping_user(companion_id, t_user_id, bot, bot_service)

    await logger.print_info(f'trying to get state user_id={companion_id}')
    companion_state_data: dict = await state.storage.get_data(user=companion_id)
    companion_state_data = await delete_button_on_previous_message(bot, companion_state_data)
    companion_state_data = await save_sending_message_attribute(companion_message, companion_state_data)

    await state.storage.set_data(user=companion_id, data=companion_state_data)

    await logger.print_info(f'send message to user_id={t_user_id}')
    return await ping_user(t_user_id, companion_id, bot, bot_service)


@logging_decorator
async def end_approve(callback: types.CallbackQuery):
    await logger.print_info(f'start end approve')
    message = callback.message
    await message.answer(
        messages['6.4'])
    return await feedback_start(callback)
