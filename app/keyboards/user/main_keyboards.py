from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class MainButtons:

    ads = InlineKeyboardButton(
        text="Объявления", callback_data="show_ads"
    )

    find_ads = InlineKeyboardButton(
        text="Найти", callback_data="find_ads"
    )

    create_ad = InlineKeyboardButton(
        text="Создать", callback_data="create_ad"
    )

    profile = InlineKeyboardButton(
        text="Профиль", callback_data="show_profile"
    )

    show_user_ads = InlineKeyboardButton(
        text="Мои объявления", callback_data="show_user_ads"
    )

    show_created_ads = InlineKeyboardButton(
        text="Созданные", callback_data="show_created_ads"
    )

    show_liked_ads = InlineKeyboardButton(
        text="Избранные", callback_data="show_like_ads"
    )

    rules = InlineKeyboardButton(
        text="Правила", callback_data="show_rules"
    )

    second_rules = InlineKeyboardButton(
        text="Далее", callback_data="show_second_rules"
    )

    to_main_menu = InlineKeyboardButton(
        text="В главное меню", callback_data="to_main_menu"
    )


class MainKeyboards:

    main_window = InlineKeyboardMarkup(
        inline_keyboard=[
            [MainButtons.ads],
            [MainButtons.profile],
            [MainButtons.rules]
        ]
    )

    ads_window = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                MainButtons.create_ad,
                MainButtons.find_ads,
            ],
            [
                MainButtons.to_main_menu
            ]
        ]
    )

    profile_window = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                MainButtons.show_user_ads
            ],
            [
                MainButtons.to_main_menu
            ]
        ]
    )

    show_user_ads = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                MainButtons.show_created_ads,
                MainButtons.show_liked_ads
            ],
            [
                MainButtons.to_main_menu
            ]
        ]
    )

    show_rules = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                MainButtons.second_rules,
            ],
            [
                MainButtons.to_main_menu
            ]
        ]
    )

    show_second_rules = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                MainButtons.to_main_menu
            ]
        ]
    )
