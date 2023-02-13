from typing import Tuple, Any, Union, Callable, List

from aiogram.types.base import Integer

from app.tgbot.models.Feedback import Feedback
from app.tgbot.models.WaitingCompanion import WaitingCompanion
from app.tgbot.repositorys.meetings_repo import MeetingRepo
from app.tgbot.repositorys.users_repo import UserRepo
from app.tgbot.repositorys.waiting_companions import WaitingCompanionRepo
from app.tgbot.repositorys.feedback_repo import FeedbackRepo

from app.tgbot.models.Criterion import Criterion
from app.tgbot.models.MyUser import MyUser
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


class BotService:

    def __init__(self, waiting_companion_repo: WaitingCompanionRepo, user_repo: UserRepo, meeting_repo: MeetingRepo,
                 feedback_repo: FeedbackRepo):
        self.waiting_companion_repo = waiting_companion_repo
        self.user_repo = user_repo
        self.meeting_repo = meeting_repo
        self.feedback_repo = feedback_repo

    @logging_decorator
    async def is_used_email(self, email: str):
        user = await self.user_repo.get_by_email(email)
        return user is not None

    @logging_decorator
    async def is_user_registered(self, t_user_id: int) -> bool:
        my_user: MyUser = await self.user_repo.get_by_t_user_id(t_user_id)
        return my_user is not None

    @logging_decorator
    async def get_user_by_t_user_id(self, t_user_id: int) -> MyUser:
        user: MyUser = await self.user_repo.get_by_t_user_id(t_user_id)
        return user

    @logging_decorator
    async def upsert_user(self, my_user: MyUser) -> bool:
        return await self.user_repo.upsert(my_user)

    @logging_decorator
    async def delete_request_for_t_user_id_with_null_status(self, t_user_id: int) -> bool:
        return await self.waiting_companion_repo.delete_request_for_t_user_id_with_null_status(t_user_id)

    #######################################################################
    @logging_decorator
    async def search_by_user(self, t_user_id: int, predicate: Callable[[Criterion, MyUser], bool], criterion: Criterion) \
            -> Union[Tuple[int, int], None]:
        """
        Support the invariant,
        if a companion is found, then no one else can invite him to a meeting.
        if a companion is not found, then our request gets into the waiting queue
        TODO tests are needed.
        :param predicate:
        :param t_user_id:
        :return: if None then companion not found, otherwise - found
        """
        await self.waiting_companion_repo.delete_request_for_t_user_id_with_null_status(t_user_id)
        user: MyUser = await self.user_repo.get_by_t_user_id(t_user_id)

        waiting_users_strangers: list[WaitingCompanion] = await self.waiting_companion_repo.get_strangers(t_user_id)
        waiting_users_strangers.sort(key=lambda x: x.time)

        waiting_users_strangers_satisfying_criterion = []

        for waiting_user in waiting_users_strangers:
            my_user: MyUser = await self.get_user_by_t_user_id(waiting_user.t_user_id)
            if predicate(waiting_user.criterion, my_user):
                waiting_users_strangers_satisfying_criterion.append(waiting_user)

        for waiting_user in waiting_users_strangers_satisfying_criterion:
            assert waiting_user.t_user_id != user.t_user_id
            if await self.try_lock_waiting_companions(user.t_user_id, waiting_user.t_user_id):
                return waiting_user.t_user_id, waiting_user.id

        success = await self.try_add_waiting_user(t_user_id, criterion)
        if success:
            await logger.print_info(f'user {t_user_id} now is in the waiting list')
        else:
            await logger.print_error(f'FAILURE while adding user {t_user_id} to waiting list')

        return None

    @logging_decorator
    async def is_strangers(self, user_id: int, companion_id: int) -> bool:
        first_user_id, second_user_id = (user_id, companion_id) if user_id < companion_id else (companion_id, user_id)
        first_meeting: list = await self.meeting_repo.get_by_members(first_user_id, second_user_id)
        return len(first_meeting) == 0

    @logging_decorator
    async def find_users_by_waiting_id(self, waiting_id: int):
        res = await self.waiting_companion_repo.get_users_by_waiting_id(waiting_id)
        return res.t_user_id, res.status

    @logging_decorator
    async def add_meeting(self, user_id: int, companion_id: int, waiting_id: int) -> bool:
        first_user_id, second_user_id = (user_id, companion_id) if user_id < companion_id else (companion_id, user_id)
        res = await self.meeting_repo.add_meeting(first_user_id, second_user_id, waiting_id)
        return res is not None

    @logging_decorator
    async def add_meeting_by_waiting_id(self, waiting_id: int) -> bool:
        user_1, user_2 = await self.find_users_by_waiting_id(waiting_id)
        assert user_1 is not None and user_2 is not None
        res = await self.add_meeting(user_1, user_2, waiting_id)
        return res

    @logging_decorator
    async def try_lock_waiting_companions(self, user_id: int, waiting_user: int) -> bool:
        res: str = await self.waiting_companion_repo.try_lock_user(user_id, waiting_user)
        await logger.print_dev(f'trying to lock {user_id} to {waiting_user} with res {res}')
        return res == 'UPDATE 1'

    #######################################################################
    @logging_decorator
    async def try_add_waiting_user(self, t_user_id: int, criterion: Criterion) -> bool:
        my_user: MyUser = await self.user_repo.get_by_t_user_id(t_user_id)
        res = await self.waiting_companion_repo.add_waiting_companion(my_user.t_user_id,
                                                                      criterion.value)
        return res == 'INSERT 0 1'

    @logging_decorator
    async def is_user_waiting_companion(self, t_user_id: int) -> bool:
        old_waiting_record = await self.waiting_companion_repo.get_by_user_id_with_null_status(t_user_id)
        return old_waiting_record is not None

    @logging_decorator
    async def is_waiting_companion_user(self, t_user_id: int) -> bool:
        old_waiting_record = await self.waiting_companion_repo.get_by_user_id_with_null_status(t_user_id)
        return old_waiting_record is not None

    @logging_decorator
    async def add_feedback(self, feedback: Feedback) -> bool:
        return await self.feedback_repo.add_feedback(feedback)

    @logging_decorator
    async def all_feedback_by_t_user_id(self, t_user_id: int) -> List[Feedback]:
        return await self.feedback_repo.all_feedback_by_t_user_id(t_user_id)
