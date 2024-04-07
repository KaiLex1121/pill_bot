from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from app.enums.advertisment import TypeOfAd


class AdTypeFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == "take":
            return {'ad_type_enum': TypeOfAd.take.value}
        elif callback.data == "give":
            return {'ad_type_enum': TypeOfAd.give.value}
        elif callback.data == "all_ad_types":
            return {'ad_type_enum': 'all_ad_types'}
        else:
            return False
