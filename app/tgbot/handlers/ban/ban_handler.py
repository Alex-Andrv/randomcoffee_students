from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, User

from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.message_loader import messages

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


class BanStates(StatesGroup):
    ban_state = State()


@logging_decorator
async def user_ban_handler(to: Message | CallbackQuery, bot_service: BotService, state: FSMContext):
    user: User = User.get_current()
    await bot_service.delete_user_from_queue(user.id)
    await state.set_state(None)
    await state.set_data(None)
    bot: Bot = to.bot
    return await bot.send_message(user.id, messages['11'])
