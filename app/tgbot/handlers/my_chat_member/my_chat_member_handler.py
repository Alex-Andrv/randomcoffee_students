from aiogram.types import ChatMemberUpdated

from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


@logging_decorator
async def stop_bot_event_handler(update: ChatMemberUpdated, bot_service: BotService):
    user = update.from_user
    t_user_id = user.id
    old_chat_member = update.old_chat_member
    new_chat_member = update.new_chat_member
    old_chat_member_status = old_chat_member.status
    new_chat_member_status = new_chat_member.status
    await logger.print_info(f"old user = {t_user_id} status was '{old_chat_member_status} ")
    await logger.print_info(f"new user = {t_user_id} status is '{new_chat_member_status} ")
    if new_chat_member_status == "kicked":
        from app.__main__ import storage
        await storage.set_state(user=t_user_id)  # set state user to null
        await storage.set_data(user=t_user_id)  # set data user to null
        await logger.print_info(f"free user storage user = {t_user_id} ")
        await bot_service.waiting_companion_repo.delete_request_for_t_user_id_with_null_status(t_user_id)
        await logger.print_info(f"delete_request_for_t_user_id_with_null_status for 'kicked' user = {t_user_id}")
