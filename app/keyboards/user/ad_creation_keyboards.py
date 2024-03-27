from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class AdCreationButtons:

    show_ad_preview = InlineKeyboardButton(
        text='Показать анкету', callback_data="show_ad_preview"
    )

    first_delivery_type = InlineKeyboardButton(
        text="Встреча", callback_data="meeting"
    )

    second_delivery_type = InlineKeyboardButton(
        text="Доставка", callback_data="delivery"
    )

    first_ad_type = InlineKeyboardButton(
        text="Возьму", callback_data="take"
    )

    second_ad_type = InlineKeyboardButton(
        text="Отдам", callback_data="give"
    )

    to_main_menu = InlineKeyboardButton(
        text="В главное меню", callback_data="to_main_menu"
    )


class AdCreationKeyboards:

    show_ad_preview = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                AdCreationButtons.show_ad_preview
            ],
            [
                AdCreationButtons.to_main_menu
            ]
        ]
    )

    fill_delivery_type = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                AdCreationButtons.first_delivery_type,
                AdCreationButtons.second_delivery_type
            ],
            [
                AdCreationButtons.to_main_menu
            ]
        ]
    )

    fill_ad_type = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                AdCreationButtons.first_ad_type,
                AdCreationButtons.second_ad_type,
            ],
            [AdCreationButtons.to_main_menu],
        ]
    )

    to_main_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                AdCreationButtons.to_main_menu
            ]
        ]
    )
