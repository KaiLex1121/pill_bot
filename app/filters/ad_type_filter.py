from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from app.enums.advertisment import TypeOfAd


class AdTypeFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == "take":
            return {'ad_type_enum': TypeOfAd.take}
        elif callback.data == "give":
            return {'ad_type_enum': TypeOfAd.give}
        else:
            return False
