import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from aiogram.types import User

from app.tgbot.utils.BotLogger import BotLogger

global_lock = {}

logger = BotLogger(name=__name__)


class BarrierPre(LifetimeControllerMiddleware):
    """
    Barrier - ensures that only 1 handler is executed for a particular user
    """
    skip_patterns = ["error", "update"]

    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        super().__init__()

    async def pre_process(self, obj, data, *args):
        user: User = types.User.get_current()
        user_id = user.id
        if user_id not in global_lock:
            global_lock[user_id] = asyncio.Lock()

        lock = global_lock[user_id]

        if lock.locked():
            raise CancelHandler("skip unnecessary update")

        await lock.acquire()

        await logger.print_info(f"User acquire lock {user_id}")

    async def post_process(self, obj, data, *args):
        pass
    #     aiogram исполняет post хандлеры в том же порядке, что и pre, поэтому освобождение надо делать в BarrierPost


class BarrierPost(LifetimeControllerMiddleware):
    """
    Barrier - ensures that only 1 handler is executed for a particular user
    """

    skip_patterns = ["error", "update"]

    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        super().__init__()

    async def pre_process(self, obj, data, *args):
        pass
    #     aiogram исполняет pre хандлеры в том же порядке, что и post, поэтому освобождение надо делать в BarrierPre

    async def post_process(self, obj, data, *args):
        user: User = types.User.get_current()
        user_id = user.id

        lock = global_lock[user_id]
        lock.release()
        await logger.print_info(f"User release lock {user_id}")
#     TODO need release lock in error handle, error can raise in another middleware,
#      than user will be locked all time.
#     I probably managed to fix it. In error handler we almost certainly release lock
