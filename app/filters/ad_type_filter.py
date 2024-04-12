from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from app.enums.advertisment import TypeOfAd


class AdTypeFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == "take" or callback.data == "give" or callback.data == "all_ad_types":
            return True
        return False
