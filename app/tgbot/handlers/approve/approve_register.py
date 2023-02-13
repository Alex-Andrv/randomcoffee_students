from aiogram import Dispatcher

from app.tgbot.handlers.approve.approve_handlers import ApproveStates, end_approve


def register_approve(dp: Dispatcher):
    dp.register_callback_query_handler(
        end_approve,
        state=ApproveStates.approve,
        text="confirm")
