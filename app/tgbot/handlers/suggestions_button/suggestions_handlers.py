from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from typeguard import check_type

from app.tgbot.exseptions.exseptions import NotFoundInState
from app.tgbot.models.MyMessage import MyMessage
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.message_loader import messages
from app.tgbot.utils.state_access_wrapper import get_attr_from_state_with_default, \
    set_attr_to_state


class SuggestionStates(StatesGroup):
    reading_suggestion = State()


logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


@logging_decorator
async def send_suggestion(message: types.Message, state: FSMContext):
    message_before_interruption: MyMessage = \
        MyMessage.from_dict(await get_attr_from_state_with_default(state, 'message_before_interruption', None))
    state_before_interruption: str | None = \
        await get_attr_from_state_with_default(state, 'state_before_interruption', None)

    if message_before_interruption is None:
        previous_message: MyMessage = \
            MyMessage.from_dict(await get_attr_from_state_with_default(state, 'previous_message', None))

        if previous_message:
            check_type('previous_message', previous_message, MyMessage)
            curr_state: str | None = await state.get_state()
            if curr_state:
                # NOTE state can be NONE
                await set_attr_to_state(state, 'state_before_interruption', curr_state)
            await set_attr_to_state(state, 'message_before_interruption', previous_message.to_dict())
        else:
            await logger.print_error(
                f"Can't find previous_message in state: to = {message}")
            raise NotFoundInState(f"Can't find previous_message in state: to = {message}")
    else:
        check_type('message_before_interruption', message_before_interruption, MyMessage)
        check_type('state_before_interruption', state_before_interruption, str | None)

    await SuggestionStates.reading_suggestion.set()
    return await message.answer(messages['10.1'])


@logging_decorator
async def read_suggestion(message: types.Message, state: FSMContext):
    await logger.send_suggestion(message.text)

    message_before_interruption: MyMessage = \
        MyMessage.from_dict(await get_attr_from_state_with_default(state, 'message_before_interruption', None))
    state_before_interruption: str | None = \
        await get_attr_from_state_with_default(state, 'state_before_interruption', None)

    if message_before_interruption is None:
        await logger.print_error(
            f"Can't find message_before_interruption in state: to = {message}")
        raise NotFoundInState(f"Can't find message_before_interruption in state: to = {message}")

    if state_before_interruption is None:
        await logger.print_warning(f"state_before_interruption in None")

    check_type('message_before_interruption', message_before_interruption, MyMessage)
    check_type('state_before_interruption', state_before_interruption, str | None)

    await set_attr_to_state(state, 'message_before_interruption', None)

    await state.set_state(state_before_interruption)

    await message.answer(messages['10.2'])

    bot: Bot = message.bot
    return await bot.send_message(
        chat_id=message_before_interruption.chat_id,
        text=message_before_interruption.text,
        reply_markup=
        message_before_interruption.reply_markup if message_before_interruption.with_reply_markup else None,
        parse_mode=message_before_interruption.parse_mode)
