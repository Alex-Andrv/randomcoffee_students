from datetime import datetime, timedelta

from aiogram import types
from aiogram.types import User

from app.tgbot.handlers.ready.ready_handlers import ask_start_conversation
from app.tgbot.handlers.ready.ready_keyboards import cancel_queue_buttons
from app.tgbot.handlers.ready.ready_state import ReadyStates
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.message_loader import messages

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


def timestamp_to_week_day(timestamp: datetime):
    # Используем функцию weekday() для получения номера дня недели (понедельник = 0, воскресенье = 6)
    weekday_num = timestamp.weekday()
    day_name = ["понедельник", "вторник", "среду", "четверг", "пятницу", "субботу", "воскресенье"]

    # Используем список calendar.day_name для получения названия дня недели на основе номера
    return day_name[weekday_num]



@logging_decorator
async def start_conversation_new(callback: types.CallbackQuery, bot_service: BotService):
    t_user_id = User.get_current().id
    matching_date = timestamp_to_week_day(await bot_service.add_user_to_queue_and_get_matching_date(t_user_id))
    await logger.print_info("user added to queue")
    message = callback.message
    await ReadyStates.add_to_queue.set()
    return await message.answer(
        messages['4.12'].format(matching_date=matching_date), reply_markup=cancel_queue_buttons)


@logging_decorator
async def cancel_queue(callback: types.CallbackQuery, bot_service: BotService):
    t_user_id = User.get_current().id
    message = callback.message
    matching_time: datetime = await bot_service.get_matching_time_by_t_user_id(t_user_id)
    now: datetime = datetime.now()
    await logger.print_info("try delete user from queue")
    if matching_time - now < timedelta(minutes = 130):
        await logger.print_info("can't delete from queue")
        return await message.answer(
            messages['4.15'])
    else:
        await logger.print_info("seduced delete from queue")
        await bot_service.delete_user_from_queue(t_user_id)
        await message.answer(messages['4.14'])
        return await ask_start_conversation(message.bot)