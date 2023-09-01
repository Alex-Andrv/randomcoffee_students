from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import User

from app.tgbot.exseptions.exseptions import NotFoundInState
from app.tgbot.handlers.itmoId.itmoid_keyboard import get_itmoid_keyboard
from app.tgbot.handlers.registration.registration_handlers import ask_for_info, ask_is_student, RegistrationStates
from app.tgbot.models.Criterion import CriterionBuilder
from app.tgbot.models.IsuData import IsuData
from app.tgbot.models.MyUser import MyUserBuilder, Role
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory
from app.tgbot.utils.message_loader import messages
from app.tgbot.utils.state_access_wrapper import set_attr_to_state

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


class ItmoIdStates(StatesGroup):
    OAuth_start = State()


# NOT A HANDLER;
@logging_decorator
async def offer_oauth(callback: types.CallbackQuery):
    await ItmoIdStates.OAuth_start.set()
    bot: Bot = callback.bot
    user_id: int = User.get_current().id
    return await bot.send_message(user_id, messages['21.1'], reply_markup=get_itmoid_keyboard(user_id))


@logging_decorator
async def validate_oauth(callback: types.CallbackQuery, bot_service: BotService, state: FSMContext):
    t_user_id: int = User.get_current().id
    isudata: IsuData = await bot_service.get_isu_data(t_user_id)
    if isudata:
        user_builder: MyUserBuilder = MyUserBuilder()
        user_builder.set_t_user_id(t_user_id)
        user_builder.set_email(isudata.email)
        user_builder.set_full_name(isudata.name)
        user_builder.set_sex(isudata.gender)
        user_builder.set_is_student(isudata.is_student)
        user_builder.set_is_work(isudata.is_worker)

        if (await bot_service.is_user_registered(t_user_id)) and (await bot_service.is_old_user(t_user_id)):
            myUser = await bot_service.get_user_by_t_user_id(t_user_id)
            user_builder.set_user_info(myUser.user_info)
        
        await set_attr_to_state(state, 'criterion_builder', CriterionBuilder(t_user_id).to_dict())

        if not (isudata.is_worker or isudata.is_student):
            await logger.print_error(f"user = {t_user_id}, sub = {isudata.sub}, isu = {isudata.isu}, name = {isudata.name} not student and not worker")
            raise NotFoundInState(f"user = {t_user_id}, sub = {isudata.sub}, isu = {isudata.isu}, name = {isudata.name} not student and not worker")

        user_builder.set_user_name(User.get_current().username)

        if not (user_builder.is_worker and user_builder.is_student):
            user_builder.set_role(Role.STUDENT if user_builder.is_student else Role.WORKER)
            await set_attr_to_state(state, 'user_builder', user_builder.to_dict())
            return await ask_for_info(callback.message, bot_service)

        await set_attr_to_state(state, 'user_builder', user_builder.to_dict())
        return await ask_is_student(callback.message)
        # return await ask_for_name(callback.message, bot_service, state)
    else:
        return await offer_oauth(callback)
