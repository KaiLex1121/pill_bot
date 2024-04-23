from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.keyboards.user import AdSearchKeyboards


class AdModerationButtons:

    ad_search_buttons = AdSearchKeyboards.found_ad_window.inline_keyboard

    moderate = InlineKeyboardButton(
        text="Модерирование", callback_data="moderate_ad"
    )

    ban_ad_owner = InlineKeyboardButton(
        text="Заблокировать пользователя", callback_data="ban_ad_owner"
    )

    unban_ad_owner = InlineKeyboardButton(
        text="Разблокировать пользователя", callback_data="unban_ad_owner"
    )

    hide_ad = InlineKeyboardButton(
        text="Удалить объявление", callback_data="hide_ad"
    )

    unhide_ad = InlineKeyboardButton(
        text="Восстановить объявление", callback_data="unhide_ad"
    )


class AdModerationKeyboards:

    ad_moderation = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    AdModerationButtons.moderate
                ]
            ]
    )

    moderation_panel = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    AdModerationButtons.ban_ad_owner,
                    AdModerationButtons.unban_ad_owner,
                ],
                [
                    AdModerationButtons.hide_ad,
                    AdModerationButtons.unhide_ad
                ]
            ]
    )
