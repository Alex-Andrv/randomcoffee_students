from aiogram import Dispatcher
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import User

from app.tgbot.models.MyUser import MyUser, MyUserBuilder
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger

logger = BotLogger(__name__)


class UpdateUsernameMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update", "my_chat_member"]

    def __init__(self, dispatcher: Dispatcher):
        super().__init__()
        self.dispatcher = dispatcher

    async def pre_process(self, obj, data, *args):
        user: User = User.get_current()
        bot_service: BotService = data['bot_service']
        my_user: MyUser = await bot_service.get_user_by_t_user_id(user.id)
        if my_user and (my_user.user_name != user.username) and (user.username is not None):
            user_builder: MyUserBuilder = MyUserBuilder.from_user(my_user)
            user_builder.set_user_name(user.username)
            await bot_service.upsert_user(user_builder.to_user())
            await logger.print_info(f"username t_user_id={user.id} is updated successfully")

