from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import User

from app.tgbot.handlers.feedback.feedback_keyboard import feedback_like_buttons, feedback_problem_buttons, \
    feedback_button, feedback_loose_buttons, feedback_forced_buttons
from app.tgbot.handlers.ready.ready_handlers import ask_start_conversation
from app.tgbot.models.Feedback import FeedbackBuilder
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.Validate import Validate
from app.tgbot.utils.message_loader import messages


class FeedbackStates(StatesGroup):
    basic_feedback = State()  # will gently ask to give some feedback
    aggressive_feedback = State()  # will ask to give feedback but no 'later' option
    reading_like = State()  # will remind to leave a like
    finding_problem = State()  # will remind to select the type of problem
    reading_problem = State()  # will remind to FUCKING WRITE
    reading_bot_problem = State()  # will remind to write


logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


@logging_decorator
async def feedback_start(callback: types.CallbackQuery):
    await logger.print_info(f'user {callback.from_user.id} started feedback')
    return await ask_for_feedback(callback.message)


@logging_decorator
async def ask_for_feedback_test(message: types.Message):
    await FeedbackStates.basic_feedback.set()
    await logger.print_warning(f'user {User.get_current().id} using test-only feature "/test_feedback"')
    return await message.answer(messages['7.1'].format(link='https://telegra.ph/Kommunikativnye-lajfhaki-02-22'),
                                reply_markup=feedback_button,
                                parse_mode='Markdown')


@logging_decorator
async def ask_for_feedback(message: types.Message):
    await FeedbackStates.basic_feedback.set()
    return await message.answer(messages['7.1'].format(link='https://telegra.ph/Kommunikativnye-lajfhaki-02-22'),
                                reply_markup=feedback_button,
                                parse_mode='Markdown')


@logging_decorator
async def feedback(callback: types.CallbackQuery):
    await FeedbackStates.basic_feedback.set()
    return await callback.message.answer(messages['7.3'], reply_markup=feedback_loose_buttons)


@logging_decorator
async def feedback_now(callback: types.CallbackQuery):
    await FeedbackStates.aggressive_feedback.set()
    return await callback.message.answer(messages['7.3'], reply_markup=feedback_forced_buttons)


@logging_decorator
async def proceed_to_like(callback: types.CallbackQuery):
    await FeedbackStates.reading_like.set()
    await logger.print_info(f'user {callback.from_user.id} wants to like')
    return await callback.message.answer(messages['7.8'], reply_markup=feedback_like_buttons)


@logging_decorator
async def proceed_to_problem(callback: types.CallbackQuery):
    await FeedbackStates.finding_problem.set()
    await logger.print_info(f'user {callback.from_user.id} wants to send a problem')
    return await callback.message.answer(messages['7.16'], reply_markup=feedback_problem_buttons)


@logging_decorator
async def pause_feedback(callback: types.CallbackQuery):
    await FeedbackStates.aggressive_feedback.set()
    await logger.print_info(f'user {callback.from_user.id} is not decided on his feedback yet')
    return await callback.message.answer(messages['7.11'], reply_markup=feedback_button)


@logging_decorator
async def read_like(callback: types.CallbackQuery, state: FSMContext, bot_service: BotService):
    t_user_id = callback.from_user.id
    num_of_likes = int(callback.data[:1])
    await logger.print_dev(f'writing to db: {callback.data[:1]} likes')

    meeting_id: int = await bot_service.get_last_meeting_id_by_t_user_id(t_user_id)
    feedback_builder: FeedbackBuilder = FeedbackBuilder() \
        .set_rating(num_of_likes) \
        .set_t_user_id(t_user_id) \
        .set_is_meeting_took_place(True) \
        .set_meeting_id(meeting_id)
    await bot_service.add_feedback(feedback_builder.to_feedback())
    await callback.message.answer(messages['7.10'])
    return await ask_start_conversation(callback.message.bot)


@logging_decorator
async def read_classified_problem(callback: types.CallbackQuery, state: FSMContext, bot_service: BotService):
    t_user_id = callback.from_user.id
    await logger.print_dev(f'writing to db: classified problem: {callback.data}')

    meeting_id: int = await bot_service.get_last_meeting_id_by_t_user_id(t_user_id)
    feedback_builder: FeedbackBuilder = FeedbackBuilder() \
        .set_cancellation_reason(callback.data) \
        .set_t_user_id(t_user_id) \
        .set_is_meeting_took_place(False) \
        .set_meeting_id(meeting_id)
    await bot_service.add_feedback(feedback_builder.to_feedback())
    await callback.message.answer(messages['7.21'])
    return await ask_start_conversation(callback.message.bot)


@logging_decorator
async def proceed_to_bot_problem(callback: types.CallbackQuery):
    await FeedbackStates.reading_bot_problem.set()
    return await callback.message.answer(messages['7.20.1'])


@logging_decorator
async def proceed_to_describing_problem(callback: types.CallbackQuery):
    await FeedbackStates.reading_problem.set()
    return await callback.message.answer(messages['7.19.1'])


@logging_decorator
async def read_bot_problem(message: types.Message, state: FSMContext, bot_service: BotService):
    if not await Validate.validate_text(message.text):
        await message.answer(messages['3.11.1.1'])
        await FeedbackStates.finding_problem.set()
        await logger.print_info(f'user {message.from_user.id} wants to send a problem')
        return await message.answer(messages['7.16'], reply_markup=feedback_problem_buttons)

    t_user_id = User.get_current().id
    await logger.print_dev(f'writing to db: bot problem: {message.text}')
    meeting_id: int = await bot_service.get_last_meeting_id_by_t_user_id(t_user_id)
    feedback_builder: FeedbackBuilder = FeedbackBuilder() \
        .set_cancellation_reason('(!) bot problem: ' + message.text) \
        .set_t_user_id(t_user_id) \
        .set_is_meeting_took_place(False) \
        .set_meeting_id(meeting_id)
    await bot_service.add_feedback(feedback_builder.to_feedback())

    await message.answer(messages['7.21'])
    return await ask_start_conversation(message.bot)


@logging_decorator
async def read_other_problem(message: types.Message, state: FSMContext, bot_service: BotService):
    if not await Validate.validate_text(message.text):
        await message.answer(messages['3.11.1.1'])
        await FeedbackStates.finding_problem.set()
        await logger.print_info(f'user {message.from_user.id} wants to send a problem')
        return await message.answer(messages['7.16'], reply_markup=feedback_problem_buttons)

    t_user_id = User.get_current().id
    await logger.print_dev(f'writing to db: other problem: {message.text}')
    meeting_id: int = await bot_service.get_last_meeting_id_by_t_user_id(t_user_id)
    feedback_builder: FeedbackBuilder = FeedbackBuilder() \
        .set_cancellation_reason(message.text) \
        .set_t_user_id(t_user_id) \
        .set_is_meeting_took_place(False) \
        .set_meeting_id(meeting_id)
    await bot_service.add_feedback(feedback_builder.to_feedback())

    await message.answer(messages['7.21'])
    return await ask_start_conversation(message.bot)
