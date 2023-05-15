import asyncio
import logging

import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ContentTypes
from asyncpg import Connection

from app.configs.general_bot_config import REDIS_HOST, REDIS_PORT, REDIS_DP, REDIS_PASSWORD, DB_USER, \
    DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, BOT_TOKEN
from app.configs.log_config import LOG_LEVEL, LOG_FILENAME, LOG_FILEMODE, LOG_FORMAT
from app.tgbot.filters.is_user_have_username import IsUsernameMissingFilter
from app.tgbot.handlers.approve.approve_register import register_approve
from app.tgbot.handlers.ban.ban_register import register_user_ban
from app.tgbot.handlers.email.email_register import register_email
from app.tgbot.handlers.error.error_handler import exception_handler
from app.tgbot.handlers.feedback.feedback_register import register_feedback
from app.tgbot.handlers.itmoId.itmoid_register import register_itmoid
from app.tgbot.handlers.my_chat_member.my_chat_member_handler import stop_bot_event_handler
from app.tgbot.handlers.ready.ready_register import register_ready
from app.tgbot.handlers.registration.registration_register import register_registration
from app.tgbot.handlers.search.search_register import register_search
from app.tgbot.handlers.start.start_register import register_start
from app.tgbot.handlers.suggestions_button.suggestion_register import register_suggestion_button
from app.tgbot.handlers.unexpected_user_behavior.unexpected_user_behavior import \
    unexpected_user_behavior_message_handler, unexpected_user_behavior_callback_handler
from app.tgbot.handlers.user_have_not_username.user_have_not_username_register import register_user_have_not_username
from app.tgbot.middlewares.BanUser import BanUserMiddleware
from app.tgbot.middlewares.Barrier import BarrierPre, BarrierPost
from app.tgbot.middlewares.DependencyInjection import DependencyInjection
from app.tgbot.middlewares.RemovePreviousButtons import RemovePreviousButtons
from app.tgbot.middlewares.SkipUnnecessaryUpdate import SkipUnnecessaryUpdate
from app.tgbot.middlewares.Throttling import Throttling
from app.tgbot.middlewares.UpdateUsername import UpdateUsernameMiddleware
from app.tgbot.ui_commands import set_bot_commands
from app.tgbot.utils.BotLogger import BotLogger

logging.basicConfig(
    level=LOG_LEVEL,
    filename=LOG_FILENAME,
    filemode=LOG_FILEMODE,
    format=LOG_FORMAT)

logger = BotLogger(name=__name__, extra=None, with_user_info=False)


# postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
def create_pool():
    return asyncpg.create_pool(
        dsn=f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


def create_storage():
    return RedisStorage2(REDIS_HOST, REDIS_PORT, db=REDIS_DP, password=REDIS_PASSWORD, pool_size=10)


async def make_migration():
    connect: Connection = await asyncpg.connect(
        dsn=f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    migration = open("./app/migration/migration.sql", "r").read()
    await connect.execute(migration)
    await connect.close()


storage = create_storage()


async def run():
    await make_migration()

    # Создаем бота и диспетчер
    bot = Bot(token=BOT_TOKEN)

    # Создание диспетчера
    dp = Dispatcher(bot, storage=storage)

    # Установка команд в интерфейсе
    await set_bot_commands(bot)

    dp.filters_factory.bind(IsUsernameMissingFilter, event_handlers=[dp.message_handlers, dp.callback_query_handlers])

    dp.middleware.setup(SkipUnnecessaryUpdate())
    dp.middleware.setup(BarrierPre(dp))
    dp.middleware.setup(Throttling())
    dp.middleware.setup(RemovePreviousButtons(dp))
    dp.middleware.setup(DependencyInjection(await create_pool()))
    dp.middleware.setup(BanUserMiddleware())
    dp.middleware.setup(UpdateUsernameMiddleware())
    dp.middleware.setup(BarrierPost(dp))

    # order matters
    # suggestion first to bypass text input handlers
    register_suggestion_button(dp)
    register_user_ban(dp)
    register_start(dp)
    register_user_have_not_username(dp)
    # register_email(dp)
    register_itmoid(dp)
    register_registration(dp)
    register_ready(dp)
    register_search(dp)
    register_approve(dp)
    register_feedback(dp)
    dp.register_message_handler(unexpected_user_behavior_message_handler, state='*', content_types=ContentTypes.ANY)
    dp.register_callback_query_handler(unexpected_user_behavior_callback_handler, state='*')
    dp.register_errors_handler(exception_handler)

    dp.register_my_chat_member_handler(stop_bot_event_handler, state="*")

    # start
    try:
        logger.info("bot starting")
        await dp.start_polling()
    finally:
        logger.info("bot stopping")
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(run())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Random coffee bot was stopped!")
