from aiogram.filters.callback_data import CallbackData


class AdModerationCallbackFilter(CallbackData, prefix='admod'):
    callback_data: str
    ad_owner_id: int
    ad_id: int