from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from app.enums.advertisment import TypeOfDelivery


class DeliveryTypeFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == "meeting":
            return {'delivery_type_enum': TypeOfDelivery.meeting}
        elif callback.data == "delivery":
            return {'delivery_type_enum': TypeOfDelivery.delivery}
        else:
            return False