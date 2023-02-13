from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageToEditNotFound, MessageNotModified

from app.tgbot.exseptions.exseptions import NotFoundInState, UnexpectedCallback
from app.tgbot.models.MyMessage import MyMessage
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.state_access_wrapper import get_attr_from_state_with_default

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


@logging_decorator
async def unexpected_user_behavior_message_handler(message: Message, state: FSMContext):
    await logger.print_warning(
        f"unexpected_user_behavior_message_handler was called: message = {message}; state = {state}")
    previous_message: MyMessage = \
        MyMessage.from_dict(await get_attr_from_state_with_default(state, 'previous_message', None))
    if previous_message is None:
        await logger.print_error(
            f"Can't find previous_message in state: to = {message}")
        raise NotFoundInState(f"Can't find previous_message in user_have_not_username_handler: to = {message}")
    else:
        bot: Bot = message.bot
        return await bot.send_message(
            chat_id=previous_message.chat_id,
            text=previous_message.text,
            reply_markup=previous_message.reply_markup if previous_message.with_reply_markup else None,
            parse_mode=previous_message.parse_mode)


@logging_decorator
async def unexpected_user_behavior_callback_handler(callback: CallbackQuery):
    await logger.print_error(f"unexpected_user_behavior_callback_handler was called")
    chat_id: int = callback.message.chat.id
    user_id: int = callback.from_user.id
    previous_message_id: int = callback.message.message_id
    bot: Bot = callback.bot
    await logger.print_info(f"delete previous message for user {user_id} in unexpected_user_behavior_callback_handler")
    try:
        await bot.edit_message_reply_markup(chat_id, previous_message_id)
    except MessageToEditNotFound:
        await logger.print_error(str(MessageToEditNotFound))
    except MessageNotModified:
        await logger.print_error(str(MessageNotModified))
    raise UnexpectedCallback('unexpected callback')
