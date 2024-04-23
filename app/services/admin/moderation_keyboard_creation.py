from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.filters.ad_moderation_callback_filter import AdModerationCallbackFilter


def create_ad_moderation_keyboard(
    ad_owner_id: int,
    ad_id: int
) -> InlineKeyboardMarkup:
    ad_moderation = InlineKeyboardButton(
        text='Модерация сообщения',
        callback_data=AdModerationCallbackFilter(
            callback_data='ad_moderation',
            ad_owner_id=ad_owner_id,
            ad_id=ad_id
        ).pack()
    )
    ad_moderation_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                ad_moderation
            ]
        ]
    )
    return ad_moderation_keyboard