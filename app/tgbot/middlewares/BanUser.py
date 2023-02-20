from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import User

from app.tgbot.models.MyUser import MyUser
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger

logger = BotLogger(__name__)


class BanUserMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update", "my_chat_member"]

    def __init__(self):
        super().__init__()

    async def pre_process(self, obj, data, *args):
        user: User = User.get_current()
        bot_service: BotService = data['bot_service']
        my_user: MyUser = await bot_service.get_user_by_t_user_id(user.id)
        if my_user and my_user.ban:
            storage: FSMContext = Dispatcher.get_current().current_state()
            await storage.set_state('BanStates:ban_state')
            await logger.print_info(f"username t_user_id={user.id} is ban")

