from aiogram import Bot
from aiogram.types import User

from app.tgbot.handlers.ready.ready_keyboards import start_conversation_buttons
from app.tgbot.handlers.ready.ready_state import ReadyStates
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.message_loader import messages

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


# NOT A HANDLER;
@logging_decorator
async def ask_start_conversation(bot: Bot):
    await ReadyStates.ready.set()
    user: User = User.get_current()
    return await bot.send_message(
        user.id,
        messages['4.1'],
        reply_markup=start_conversation_buttons)
