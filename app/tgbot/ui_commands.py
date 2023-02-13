from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    commands_def = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand("suggestion", "Проблемы и пожелания")
    ]

    await bot.set_my_commands(commands_def)
