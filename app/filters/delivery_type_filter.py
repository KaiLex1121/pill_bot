from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from app.enums.advertisment import TypeOfDelivery


class DeliveryTypeFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == "meeting" or callback.data == "delivery":
            return True
        return False