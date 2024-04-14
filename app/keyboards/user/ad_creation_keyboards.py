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
        text="Найти", callback_data="take"
    )

    second_ad_type = InlineKeyboardButton(
        text="Отдать", callback_data="give"
    )

    confirm_ad_creation = InlineKeyboardButton(
        text="Сохранить объявление", callback_data="confirm_ad_creation"
    )

    cancel_ad_creation = InlineKeyboardButton(
        text="В главное меню", callback_data="cancel_ad_creation"
    )

    yes_button = InlineKeyboardButton(
        text="Да", callback_data="to_main_menu"
    )

    no_button = InlineKeyboardButton(
        text="Нет", callback_data="to_current_creation_handler"
    )


class AdCreationKeyboards:

    confirm_ad_creation = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                AdCreationButtons.confirm_ad_creation
            ],
            [
                AdCreationButtons.cancel_ad_creation
            ]
        ]
    )

    show_ad_preview = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                AdCreationButtons.show_ad_preview
            ],
            [
                AdCreationButtons.cancel_ad_creation
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
                AdCreationButtons.cancel_ad_creation
            ]
        ]
    )

    fill_ad_type = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                AdCreationButtons.first_ad_type,
                AdCreationButtons.second_ad_type
            ],
            [
                AdCreationButtons.cancel_ad_creation
            ],
        ]
    )

    to_main_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                AdCreationButtons.cancel_ad_creation
            ]
        ]
    )

    confirm_returning = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                AdCreationButtons.yes_button,
                AdCreationButtons.no_button
            ]
        ]
    )