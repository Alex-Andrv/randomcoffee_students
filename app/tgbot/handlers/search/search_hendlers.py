from typing import Callable

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import User

from app.tgbot.exseptions.exseptions import UnexpectedCallback
from app.tgbot.handlers.approve.approve_handlers import start_approve
from app.tgbot.handlers.ready.ready_handlers import ask_start_conversation
from app.tgbot.handlers.search.search_keyboard import wait_companion_button, search_format_choice_buttons
from app.tgbot.models.Criterion import Criterion
from app.tgbot.models.MyUser import MyUser
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import logging_decorator_factory, BotLogger
from app.tgbot.utils.message_loader import messages
from app.tgbot.utils.state_access_wrapper import set_attr_to_state


class SearchStates(StatesGroup):
    search_format_choice = State()
    search = State()
    wait_companion = State()


logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


# NOT A HANDLER;
@logging_decorator
async def search_format_choice_search(callback: types.CallbackQuery):
    await SearchStates.search_format_choice.set()
    message = callback.message
    return await message.answer(
        messages['5.0'], reply_markup=search_format_choice_buttons)


@logging_decorator
async def search_search(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext):
    await SearchStates.search.set()
    callback_data: str = callback.data
    bot: Bot = callback.bot
    user_id: int = User.get_current().id
    if callback_data == messages['5.0.1']:
        #     Бизнес встречи
        await logger.print_info("user choice business meeting")
        await bot.send_message(user_id, "🚀")
        return await search(callback, bot_service, state,
                            lambda c, _: c == Criterion.BUSINESS, Criterion.BUSINESS)
    elif callback_data == messages['5.0.2']:
        #     Dating
        user: User = User.get_current()
        my_user: MyUser = await bot_service.get_user_by_t_user_id(user.id)
        await logger.print_info("user choice dating meeting")
        await bot.send_message(user_id, "❤️")
        return await search(callback, bot_service, state,
                            lambda c, u: c == Criterion.DATING and u.sex == my_user.sex, Criterion.DATING)
        # специальный мем
    elif callback_data == messages['5.0.3']:
        #     Random
        await logger.print_info("user choice random meeting")
        await bot.send_dice(user_id, emoji="🎲️")
        return await search(callback, bot_service, state,
                            lambda c, _: c == Criterion.RANDOM, Criterion.RANDOM)
    elif callback_data == messages['5.0.4']:
        # Back
        await logger.print_info("user choice go back")
        return await ask_start_conversation(callback.bot)
    else:
        await logger.print_error("unexpected callback: " + callback_data + ". in search_search handler")
        raise UnexpectedCallback(callback_data + ": in search_search handler")


# NOT A HANDLER;
@logging_decorator
async def search(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext,
                 predicate: Callable[[Criterion, MyUser], bool], criterion: Criterion):
    t_user_id = callback.from_user.id
    await logger.print_info(f'user {t_user_id} is searching for companion')
    res = await bot_service.search_by_user(t_user_id, predicate, criterion)
    if res is not None:
        companion_id, meeting_id = res
        await set_attr_to_state(state, 'meeting_id', meeting_id)
        await logger.print_info(f'meeting id {meeting_id} (user: {t_user_id}) is written to data')
        await logger.print_info(f'trying to get state user_id={companion_id}')
        companion_state_data: dict = await state.storage.get_data(user=companion_id)
        companion_state_data['meeting_id'] = meeting_id
        await state.storage.set_data(user=companion_id, data=companion_state_data)
        await logger.print_info(f'meeting id {meeting_id} (user: {companion_id}) is written to data')
        return await start_approve(callback, companion_id, bot_service, state)
    else:
        return await wait_companion(callback)


@logging_decorator
async def cancel_search(callback: types.CallbackQuery, bot_service: BotService):
    user: User = User.get_current()
    result: bool = await bot_service.delete_request_for_t_user_id_with_null_status(user.id)
    if not result:
        await logger.print_error(f"can't delete_request_for_t_user_id_with_null_status for user = {user.id}")
        return
    return await search_format_choice_search(callback)


# NOT A HANDLER;
@logging_decorator
async def wait_companion(callback: types.CallbackQuery):
    await SearchStates.wait_companion.set()
    message = callback.message
    return await message.answer(
        messages['5.2'], reply_markup=wait_companion_button)
