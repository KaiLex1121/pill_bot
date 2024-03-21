from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class MainButtons:

    init_rules_check = InlineKeyboardButton(
        text="К правилам", callback_data="init_rules_check"
    )


class MainKeyboards:

    rules_check = InlineKeyboardMarkup(
        inline_keyboard=[
            [MainButtons.init_rules_check],
        ]
    )
