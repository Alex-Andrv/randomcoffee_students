from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import User

from app.tgbot.exseptions.exseptions import SMPTError
from app.tgbot.handlers.email.email_keyboard import wait_email_buttons, retry_code_buttons
from app.tgbot.models.MyUser import MyUserBuilder
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.Email import Email
from app.tgbot.utils.message_loader import messages
from app.tgbot.utils.state_access_wrapper import get_attr_from_state, set_attr_to_state

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)

MAX_ATTEMPTS = 3

email_server = Email()


class EmailStates(StatesGroup):
    reading_email = State()
    awaiting_code = State()
    wrong_code = State()
    user_banned = State()  # TIMEOUT 1 DAY


# NOT A HANDLER;
@logging_decorator
async def ask_for_email(callback: types.CallbackQuery):
    await EmailStates.reading_email.set()
    bot: Bot = callback.bot
    user_id: int = User.get_current().id
    return await bot.send_message(user_id, messages['2.1'])


@logging_decorator
async def read_email(message: types.Message, bot_service: BotService, state: FSMContext):
    email: str = message.text.strip()
    if Email.is_valid_email(email):
        is_used_email: bool = await bot_service.is_used_email(email)
        if is_used_email:
            await logger.print_warning(f'someone trying email {email} which is already registered')
            return await message.answer(messages['2.8'])
        else:
            await set_attr_to_state(state, 'email', email)
            return await send_code(message, state)
    else:
        await logger.print_warning(f'declined email {email}')
        return await message.answer(messages['2.4'])


# NOT A HANDLER;
@logging_decorator
async def send_code(message: types.Message, state: FSMContext):
    email = await get_attr_from_state(state, 'email')
    code: str = Email.generate_code()
    await set_attr_to_state(state, 'code', code)

    t_user_id: int = User.get_current().id

    try:
        await logger.print_info(f'user {t_user_id} sending {code} to {email}')
        await email_server.send_email(email, code)
    except Exception as e:
        await logger.print_error(f'failure to send email to {email} from user {t_user_id}')
        raise SMPTError(e)

    await EmailStates.awaiting_code.set()
    return await message.answer(messages['2.3'].format(email=email), reply_markup=wait_email_buttons)


@logging_decorator
async def read_code(message: types.Message, bot_service: BotService, state: FSMContext):
    t_user_id = User.get_current().id
    actual_code = message.text.strip()
    expected_code: str = await get_attr_from_state(state, 'code')

    if actual_code == expected_code:
        user_builder: MyUserBuilder = MyUserBuilder()
        user_builder.set_t_user_id(t_user_id)
        user_builder.set_email(await get_attr_from_state(state, 'email'))
        await set_attr_to_state(state, 'user_builder', user_builder.to_dict())
        await logger.print_info(f'user {t_user_id} confirmed email')
        await message.answer(text=messages['2.7'])
        # return await ask_for_name(message, bot_service, state)
    else:
        # TODO add ban
        await logger.print_warning(
            f'user {t_user_id} tried a wrong code, expected = {expected_code}, actual = {actual_code}')
        await EmailStates.wrong_code.set()
        return await message.answer(text=messages['2.10'], reply_markup=retry_code_buttons)


@logging_decorator
async def read_invalid_code(message: types.Message):
    await logger.print_dev(f'message {message.text} parsed as an invalid code')
    return await message.answer(messages['2.9'], reply_markup=wait_email_buttons)


@logging_decorator
async def retry_code(callback: types.CallbackQuery, state: FSMContext):
    await logger.print_info(f'user {callback.from_user.id} asks for code again')
    return await send_code(callback.message, state)


@logging_decorator
async def change_email(callback: types.CallbackQuery):
    await logger.print_info(f'user {callback.from_user.id} wants to change email')
    await EmailStates.reading_email.set()
    return await callback.message.answer(messages['2.2'])
