from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, User
from typeguard import check_type

from app.tgbot.exseptions.exseptions import NotFoundInState
from app.tgbot.handlers.user_have_not_username.user_have_not_username_keyboard import recheck_username_button
from app.tgbot.models.MyMessage import MyMessage
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.message_loader import messages
from app.tgbot.utils.state_access_wrapper import get_attr_from_state_with_default, set_attr_to_state

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


@logging_decorator
async def user_have_not_username_handler(to: Message | CallbackQuery, state: FSMContext):
    await logger.print_info('username missing')
    user_have_not_username_message: MyMessage = \
        MyMessage.from_dict(await get_attr_from_state_with_default(state, 'user_have_not_username_message', None))
    if user_have_not_username_message is None:
        previous_message: MyMessage = \
            MyMessage.from_dict(await get_attr_from_state_with_default(state, 'previous_message', None))
        if previous_message:
            check_type('previous_message', previous_message, MyMessage)
            await set_attr_to_state(state, 'user_have_not_username_message', previous_message.to_dict())
        else:
            await logger.print_error(
                f"Can't find previous_message in state: to = {to}")
            raise NotFoundInState(f"Can't find previous_message in state: to = {to}")
    else:
        check_type('user_have_not_username_message', user_have_not_username_message, MyMessage)

    user_id: int = User.get_current().id
    bot: Bot = to.bot
    return await bot.send_message(user_id, messages['8.1'], reply_markup=recheck_username_button, parse_mode='Markdown')


@logging_decorator
async def user_specified_username(callback: CallbackQuery, state: FSMContext):
    await logger.print_info('username specified')
    user_have_not_username_message: MyMessage = \
        MyMessage.from_dict(await get_attr_from_state_with_default(state, 'user_have_not_username_message', None))
    if user_have_not_username_message is None:
        await logger.print_error("Can't find user_have_not_username_message")
        raise NotFoundInState("Can't find user_have_not_username_message")
    else:
        check_type('user_have_not_username_message', user_have_not_username_message, MyMessage)

        await set_attr_to_state(state, 'user_have_not_username_message', None)

        previous_message: MyMessage = user_have_not_username_message
        bot: Bot = callback.bot
        return await bot.send_message(
            chat_id=previous_message.chat_id,
            text=previous_message.text,
            reply_markup=previous_message.reply_markup if previous_message.with_reply_markup else None,
            parse_mode=previous_message.parse_mode)
