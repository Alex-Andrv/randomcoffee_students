from aiogram import Bot, Dispatcher
from aiogram.types import Update

from app.tgbot.middlewares.Barrier import global_lock
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


@logging_decorator
async def exception_handler(update: Update, error):
    if update.message is not None:
        user_id = update.message.from_user.id
    elif update.callback_query is not None:
        user_id = update.callback_query.from_user.id
    elif update.my_chat_member is not None:
        user_id = update.my_chat_member.from_user.id
    else:
        await logger.print_error(f'unexpected update in error handler = {update}')
        return False

    lock = global_lock[user_id]
    if lock.locked():
        lock.release()
        await logger.print_info(f"User release lock {user_id}")
    # release lock

    from app.__main__ import storage
    await storage.set_state(user=user_id)  # set state user to null
    await storage.set_data(user=user_id)  # set data user to null

    await logger.print_error(str(error))
    await logger.print_error(f'{user_id} when send {update} get error')
    bot: Bot = update.bot
    await bot.send_message(user_id, "Неизвестная ошибка. Ваше состояние сброшено. Нажмите /start для продолжения")
    return False  # errors_handler must return True if error was handled correctly
