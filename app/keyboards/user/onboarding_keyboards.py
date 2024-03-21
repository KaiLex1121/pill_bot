from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class OnboardingButtons:

    init_rules_check = InlineKeyboardButton(
        text="К правилам",
        callback_data="init_rules_check"
    )

    last_rules_check = InlineKeyboardButton(
        text="Далее",
        callback_data="last_rules_check"
    )

    accept_rules = InlineKeyboardButton(
        text="Прочитал и принимаю",
        callback_data="rules_accepted"
    )


class OnboardingKeyboards:

    rules_check = InlineKeyboardMarkup(
        inline_keyboard=[
            [OnboardingButtons.init_rules_check],
        ]
    )

    accept_first_rules = InlineKeyboardMarkup(
        inline_keyboard=[
            [OnboardingButtons.last_rules_check],
        ]
    )

    accept_second_rules = InlineKeyboardMarkup(
        inline_keyboard=[
            [OnboardingButtons.accept_rules],
        ]
    )
