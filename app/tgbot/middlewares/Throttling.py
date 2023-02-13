import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject
from aiogram.utils.exceptions import Throttled

from app.tgbot.utils.BotLogger import BotLogger

logger = BotLogger(__name__)

DEFAULT_RATE_LIMIT = 1


class Throttling(LifetimeControllerMiddleware):
    """
    Throttling when flood occurs
    """
    skip_patterns = ["error", "update"]

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super().__init__()

    async def pre_process(self, obj: TelegramObject, data, *args):
        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()

        limit = self.rate_limit
        key = f"{self.prefix}_{type(obj).__name__}"

        # Use Dispatcher.throttle method.
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled:
            await logger.print_info("User sent too many requests, sleep 4 second")
            await asyncio.sleep(4)
