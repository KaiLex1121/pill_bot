from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class GeneralButtons:

    to_main_menu = InlineKeyboardButton(
        text="В главное меню", callback_data="to_main_menu"
    )


class GeneralKeyboards:

    to_main_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                GeneralButtons.to_main_menu
            ]
        ]
    )
