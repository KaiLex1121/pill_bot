from aiogram.filters.state import StatesGroup, State


class AdCreationStates(StatesGroup):
    ADS_WINDOW = State()
    FILL_COUNTRY = State()
    FILL_ADD_TYPE = State()
    FILL_CITY = State()
    FILL_DRUGS = State()
    FILL_DELIVERY_TYPE = State()
    FILL_ADDITIONAL_TEXT = State()
    SHOW_AD_PREVIEW = State()
    CONFIRM_AD_CREATION = State()
