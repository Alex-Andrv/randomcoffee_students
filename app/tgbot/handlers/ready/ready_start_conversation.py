from aiogram import Bot
from aiogram.types import User

from app.tgbot.handlers.ready.ready_keyboards import edit_profile_buttons
from app.tgbot.handlers.ready.ready_state import ReadyStates
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.message_loader import messages

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)

@logging_decorator
async def start_conversation_new(bot: Bot, bot_service: BotService):
    t_user_id = User.get_current().id
    matching_date = await bot_service.add_user_to_queue_and_get_matching_date(t_user_id)
    await logger.print_info("user added to queue")
    await ReadyStates.add_to_queue.set()
    return await bot.send_message(t_user_id,
                                  messages['4.12'].format(matching_date=matching_date.strftime("%Y-%m-%d")),
                                  reply_markup=edit_profile_buttons)