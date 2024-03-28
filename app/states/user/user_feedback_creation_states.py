from aiogram.filters.state import StatesGroup, State


class UserFeedbackCreationStates(StatesGroup):
    FEEDBACK_CREATION = State()