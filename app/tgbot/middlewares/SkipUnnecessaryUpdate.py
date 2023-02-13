from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from app.tgbot.utils.BotLogger import BotLogger

logger = BotLogger(name=__name__, extra=None, with_user_info=False)


class SkipUnnecessaryUpdate(LifetimeControllerMiddleware):
    """
    При добавлении нового update нужно обязательно посмотреть на данный метод (Dispatcher#process_update).
    И внимательно посмотреть на методы *get_current(), возможно они перестанут работать ожидаемым образом.
    """

    async def pre_process(self, obj, data, *args):
        if isinstance(obj, types.Update):
            update: types.Update = obj
            if update.message:
                return
            if update.callback_query:
                return
            if update.my_chat_member:
                return
            await logger.print_info(f"skip unnecessary update")
            raise CancelHandler("skip unnecessary update")
        # aiogram сделан очень интересно, сначала вызывается хандлер для Update. Он же в свою очередь вызывает
        # хандлер либо для error, либо для другого события (список всех хандлеров есть в Dispatcher#__init__). И
        # после каждого вызова notify вызываются все Middleware и фильтры. Поэтому бывают случаи, когда мы в if не
        # зайдем.

        # Вообще тут очень нужны type hints + наследование. Очень тяжело понять какие обьекты могут сюда попасть.
        # НИКОГДА НЕ ПИШИТЕ КОД НА PYTHON БЕЗ type hints
