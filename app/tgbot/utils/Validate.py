import re

from app.tgbot.utils.BotLogger import logging_decorator_factory, BotLogger

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


class Validate:
    @staticmethod
    async def validate_full_name(full_name: str) -> bool:
        if len(full_name) > 100:
            await logger.print_warning("full_name len is bigger than 100")
            return False

        _full_name_regex = re.compile(r'^[А-Яа-я ]+$')

        if re.match(_full_name_regex, full_name) is None:
            await logger.print_warning("full_name contains not valid simbols")
            return False

        return True

    @staticmethod
    async def validate_text(text: str) -> bool:
        if len(text) > 1000:
            await logger.print_warning("user_info len is bigger than 1000")
            return False

        _text_regex = re.compile(r'^[А-Яа-яA-Za-z0-9 ,.!@?]+$')

        if re.match(_text_regex, text) is None:
            await logger.print_warning("user_info contains not valid simbols")
            return False

        return True

