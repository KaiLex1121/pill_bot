from aiogram.filters.state import StatesGroup, State


class AdCreationStates(StatesGroup):
    FILL_ADD_TYPE = State()
    FILL_CITY = State()
    FILL_DRUGS = State()
    FILL_DELIVERY_TYPE = State()
    FILL_CONSTANT_NEED = State()
    FILL_ADDITIONAL_TEXT = State()
