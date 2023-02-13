from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import Message

from app.tgbot.utils.BotLogger import BotLogger
from app.tgbot.utils.delete_button import delete_button_on_previous_message
from app.tgbot.utils.save_message import save_sending_message_attribute

logger = BotLogger(__name__)


class RemovePreviousButtons(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update", "my_chat_member"]

    def __init__(self, dispatcher: Dispatcher):
        super().__init__()
        self.dispatcher = dispatcher

    async def pre_process(self, obj, data, *args):
        state: FSMContext = self.dispatcher.current_state()
        state_data: dict = await state.get_data()
        bot: Bot = obj.bot
        state_data = await delete_button_on_previous_message(bot, state_data)
        await state.set_data(state_data)

    async def post_process(self, obj, data, *args):
        state: FSMContext = self.dispatcher.current_state()
        state_data: dict = await state.get_data()
        state_data['previous_message'] = None
        if (len(args) < 1) or (len(args[0]) < 1) or (not isinstance(args[0][0], Message)):
            await logger.print_error("handler didn't return sent message")
            # TODO тут надо бы кинуть ошибку, но могу сломать барьер
            return
        message: Message = args[0][0]
        state_data = await save_sending_message_attribute(message, state_data)
        await state.set_data(state_data)
