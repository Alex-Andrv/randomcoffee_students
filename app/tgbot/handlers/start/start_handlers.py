from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from app.tgbot.handlers.email.email_handlers import ask_for_email
from app.tgbot.handlers.ready.ready_handlers import ask_start_conversation
from app.tgbot.handlers.start.start_keyboard import start_chatting_button
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.message_loader import messages


class StartStates(StatesGroup):
    start = State()


logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


@logging_decorator
async def start_chatting(message: types.Message, bot_service: BotService):
    await StartStates.start.set()
    await bot_service.add_visitor_if_not_exists(message.from_user.id)
    return await message.answer(messages['1.1'], reply_markup=start_chatting_button)


@logging_decorator
async def want_participate(callback: types.CallbackQuery, bot_service: BotService):
    t_user_id = callback.from_user.id
    if await bot_service.is_user_registered(t_user_id):
        return await ask_start_conversation(callback.bot)
    else:
        return await ask_for_email(callback)
