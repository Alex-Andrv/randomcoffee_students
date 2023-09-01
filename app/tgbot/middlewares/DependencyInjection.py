from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from app.tgbot.repositorys.confirm_isudata_repo import ConfirmIsudataRepo
from app.tgbot.repositorys.criterion_repo import CriterionRepo
from app.tgbot.repositorys.feedback_repo import FeedbackRepo
from app.tgbot.repositorys.group_repo import GroupRepo
from app.tgbot.repositorys.meetings_repo import MeetingRepo
from app.tgbot.repositorys.start_next_matching_algo_repo import NextMatchingRepo
from app.tgbot.repositorys.users_repo import UserRepo
from app.tgbot.repositorys.visitor_repo import VisitorRepo
from app.tgbot.repositorys.waiting_companions import WaitingCompanionRepo
from asyncpg import Pool

from app.tgbot.repositorys.work_place import WorkPlaceRepo
from app.tgbot.services.BotService import BotService
from app.tgbot.utils.BotLogger import BotLogger

logger = BotLogger(__name__)


class DependencyInjection(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, pool: Pool):
        super().__init__()
        self.pool = pool

    async def pre_process(self, obj, data, *args):
        db = await self.pool.acquire()
        await logger.print_info(f"User acquire connection")
        data["db"] = db
        visitor_repo = VisitorRepo(db)
        user_repo = UserRepo(db)
        feedback_repo = FeedbackRepo(db)
        meeting_repo = MeetingRepo(db)
        waiting_companion = WaitingCompanionRepo(db)
        confirm_isudata = ConfirmIsudataRepo(db)
        group_repo = GroupRepo(db)
        work_place = WorkPlaceRepo(db)
        criterion_repo = CriterionRepo(db)
        next_matching_repo = NextMatchingRepo(db)
        data['bot_service'] = BotService(
            waiting_companion,
            user_repo,
            meeting_repo,
            feedback_repo,
            visitor_repo,
            confirm_isudata,
            group_repo,
            work_place,
            criterion_repo,
            next_matching_repo)

    async def post_process(self, obj, data, *args):
        del data["bot_service"]
        db = data.get("db")
        if db:
            await self.pool.release(db)
            await logger.print_info(f"User release connection")
        #     TODO need release lock in error handle, error can raise in another middleware,
        #      than user will be locked all time
