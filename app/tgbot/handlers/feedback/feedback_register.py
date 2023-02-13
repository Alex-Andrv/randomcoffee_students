from aiogram import Dispatcher

from app.tgbot.handlers.feedback.feedback_handlers import ask_for_feedback_test, read_bot_problem, FeedbackStates, feedback, \
    read_other_problem, feedback_now, proceed_to_like, pause_feedback, proceed_to_problem, read_like, \
    proceed_to_describing_problem, proceed_to_bot_problem, read_classified_problem


def register_feedback(dp: Dispatcher):
    # TEST ONLY
    # dp.register_message_handler(
    #     ask_for_feedback_test,
    #     commands=["test_feedback"],
    #     state='*')

    dp.register_message_handler(
        read_bot_problem,
        state=FeedbackStates.reading_bot_problem)
    dp.register_message_handler(
        read_other_problem,
        state=FeedbackStates.reading_problem)

    dp.register_callback_query_handler(
        feedback,
        text='feedback',
        state=FeedbackStates.basic_feedback)

    dp.register_callback_query_handler(
        feedback_now,
        text='feedback',
        state=FeedbackStates.aggressive_feedback)

    dp.register_callback_query_handler(
        proceed_to_like,
        text='confirm',
        state=FeedbackStates.basic_feedback)

    dp.register_callback_query_handler(
        proceed_to_like,
        text='confirm',
        state=FeedbackStates.aggressive_feedback)

    dp.register_callback_query_handler(
        pause_feedback,
        text='unknown',
        state=FeedbackStates.basic_feedback)

    dp.register_callback_query_handler(
        proceed_to_problem,
        text='didnt_meet',
        state=FeedbackStates.basic_feedback)

    dp.register_callback_query_handler(
        proceed_to_problem,
        text='didnt_meet',
        state=FeedbackStates.aggressive_feedback)

    dp.register_callback_query_handler(
        read_like,
        state=FeedbackStates.reading_like)

    dp.register_callback_query_handler(
        proceed_to_describing_problem,
        text='other_problem',
        state=FeedbackStates.finding_problem)

    dp.register_callback_query_handler(
        proceed_to_bot_problem,
        text='bot_problem',
        state=FeedbackStates.finding_problem)

    dp.register_callback_query_handler(
        read_classified_problem,
        state=FeedbackStates.finding_problem)
