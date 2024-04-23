from aiogram.filters.state import StatesGroup, State


class AdministrationMainStates(StatesGroup):
    FILL_USERNAME_TO_BAN = State()
    FILL_USERNAME_TO_UNBAN = State()