from datetime import datetime
from typing import Tuple, Union, Callable, List

from app.tgbot.models.Feedback import Feedback
from app.tgbot.models.WaitingCompanion import WaitingCompanion
from app.tgbot.repositorys.confirm_isudata_repo import ConfirmIsudataRepo
from app.tgbot.repositorys.criterion_repo import CriterionRepo
from app.tgbot.repositorys.group_repo import GroupRepo
from app.tgbot.repositorys.meetings_repo import MeetingRepo
from app.tgbot.repositorys.start_next_matching_algo_repo import NextMatchingRepo
from app.tgbot.repositorys.users_repo import UserRepo
from app.tgbot.repositorys.visitor_repo import VisitorRepo
from app.tgbot.repositorys.waiting_companions import WaitingCompanionRepo
from app.tgbot.repositorys.feedback_repo import FeedbackRepo

from app.tgbot.models.Criterion import Criterion
from app.tgbot.models.MyUser import MyUser
from app.tgbot.repositorys.work_place import WorkPlaceRepo
from app.tgbot.utils.BotLogger import BotLogger, logging_decorator_factory

logger = BotLogger(__name__)

logging_decorator = logging_decorator_factory(logger)


class BotService:

    def __init__(self, waiting_companion_repo: WaitingCompanionRepo, user_repo: UserRepo, meeting_repo: MeetingRepo,
                 feedback_repo: FeedbackRepo, visitor_repo: VisitorRepo, confirm_isudata_repo: ConfirmIsudataRepo,
                 group_repo: GroupRepo, work_place: WorkPlaceRepo, criterion_repo: CriterionRepo,
                 next_matching_repo: NextMatchingRepo):
        self.waiting_companion_repo = waiting_companion_repo
        self.user_repo = user_repo
        self.meeting_repo = meeting_repo
        self.feedback_repo = feedback_repo
        self.visitor_repo = visitor_repo
        self.confirm_isudata_repo = confirm_isudata_repo
        self.group_repo = group_repo
        self.work_place = work_place
        self.criterion_repo = criterion_repo
        self.next_matching_repo = next_matching_repo


    @logging_decorator
    async def is_used_email(self, email: str):
        user = await self.user_repo.get_by_email(email)
        return user is not None

    @logging_decorator
    async def is_user_registered(self, t_user_id: int) -> bool:
        my_user: MyUser = await self.user_repo.get_by_t_user_id(t_user_id)
        return my_user is not None

    @logging_decorator
    async def is_old_user(self, t_user_id: int) -> bool:
        my_user: MyUser = await self.user_repo.get_by_t_user_id(t_user_id)
        return my_user is not None and my_user.old_user

    @logging_decorator
    async def get_user_by_t_user_id(self, t_user_id: int) -> MyUser:
        user: MyUser = await self.user_repo.get_by_t_user_id(t_user_id)
        return user

    @logging_decorator
    async def upsert_user(self, my_user: MyUser) -> bool:
        return await self.user_repo.upsert(my_user)


    #######################################################################

    @logging_decorator
    async def add_feedback(self, feedback: Feedback) -> bool:
        return await self.feedback_repo.add_feedback(feedback)

    @logging_decorator
    async def all_feedback_by_t_user_id(self, t_user_id: int) -> List[Feedback]:
        return await self.feedback_repo.all_feedback_by_t_user_id(t_user_id)

    @logging_decorator
    async def add_visitor_if_not_exists(self, t_user_id):
        return await self.visitor_repo.insert_if_not_exists(t_user_id)

    ####################################
    @logging_decorator
    async def get_isu_data(self, t_user_id: int):
        return await self.confirm_isudata_repo.get_isu_data(t_user_id)

    #####################################

    @logging_decorator
    async def get_grop_by_t_user_id(self, t_user_id: int):
        return await self.group_repo.get_group_by_t_user_id(t_user_id)

    #####################################

    @logging_decorator
    async def get_work_places_by_t_user_id(self, t_user_id: int):
        return await self.work_place.get_work_place_by_t_user_id(t_user_id)

    #####################################
    @logging_decorator
    async def get_criterion_by_t_user_id(self, t_user_id: int):
        return await self.criterion_repo.get_criterion_by_t_user_id(t_user_id)

    @logging_decorator
    async def upsert_criterion(self, criterion: Criterion) -> bool:
        return await self.criterion_repo.upsert(criterion)

    #####################################

    @logging_decorator
    async def add_user_to_queue_and_get_matching_date(self, t_user_id: int):
        # start transaction
        time: datetime = await self.next_matching_repo.next_matching()
        await self.waiting_companion_repo.upsert_user_in_queue(t_user_id, time)
        # end transaction
        return time

    @logging_decorator
    async def delete_user_from_queue(self, t_user_id: int):
        return await self.waiting_companion_repo.delete_user_from_queue(t_user_id)

    async def get_matching_time_by_t_user_id(self, t_user_id: int):
        return await self.waiting_companion_repo.get_matching_time_by_t_user_id(t_user_id)

    #######################################

    async def get_next_matching_time(self):
        return await self.next_matching_repo.next_matching()

    ########################################

    async def get_last_meeting_id_by_t_user_id(self, t_user_id):
        return await self.meeting_repo.get_last_meeting_id(t_user_id)

