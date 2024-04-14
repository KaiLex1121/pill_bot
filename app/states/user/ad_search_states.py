from aiogram.filters.state import StatesGroup, State


class AdSearchStates(StatesGroup):
    FILL_CITY = State()
    FILL_DRUGS = State()
    CONFIRM_AD_SEARCH = State()
    SHOW_FOUND_ADS = State()
    SHOW_NEXT_AD = State()