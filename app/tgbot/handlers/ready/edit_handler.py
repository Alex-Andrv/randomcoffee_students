from aiogram import types
from aiogram.dispatcher import FSMContext

from app.tgbot.handlers.registration.registration_handlers import ask_for_name
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import logging_decorator_factory, BotLogger

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


@logging_decorator
async def edit_profile(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext):
    t_user_id: int = callback.from_user.id
    await logger.print_info(f'user {t_user_id} is editing profile')
    return await ask_for_name(callback.message, bot_service, state)
