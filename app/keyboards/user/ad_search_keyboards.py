from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class _AdSearchButtons:

    cancel_ad_search = InlineKeyboardButton(
        text="В главное меню", callback_data="cancel_ad_search"
    )

    yes_button = InlineKeyboardButton(
        text="Да", callback_data="to_main_menu"
    )

    no_button = InlineKeyboardButton(
        text="Нет", callback_data="to_current_handler"
    )

    confirm_and_find_ads = InlineKeyboardButton(
        text="Искать объявления",
        callback_data="confirm_and_find_ads"
    )

    show_next_ad = InlineKeyboardButton(
        text="Следующее", callback_data="show_next_ad"
    )

    like = InlineKeyboardButton(
        text="Лайк", callback_data="like"
    )

    report = InlineKeyboardButton(
        text="Репорт", callback_data="report"
    )


class AdSearchKeyboards:

    like_and_report = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                _AdSearchButtons.like,
                _AdSearchButtons.report
            ],
        ]
    )

    ad_window = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                _AdSearchButtons.show_next_ad,
            ],
            [
                _AdSearchButtons.like,
                _AdSearchButtons.report
            ],
            [
                _AdSearchButtons.cancel_ad_search
            ],
        ]
    )

    find_ads = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                _AdSearchButtons.confirm_and_find_ads,
            ],
            [
                _AdSearchButtons.cancel_ad_search
            ],
        ]
    )

    to_main_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                _AdSearchButtons.cancel_ad_search
            ]
        ]
    )

    confirm_returning = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                _AdSearchButtons.yes_button,
                _AdSearchButtons.no_button
            ]
        ]
    )