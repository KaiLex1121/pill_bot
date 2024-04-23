from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.keyboards.user import MainKeyboards
from app.keyboards.general_keyboards import GeneralButtons


class AdminMainButtons:

    main_window_buttons = MainKeyboards.main_window.inline_keyboard

    administer = InlineKeyboardButton(
        text="Администрирование", callback_data="administer_bot"
    )

    statistic = InlineKeyboardButton(
        text="Статистика", callback_data="get_statistic"
    )

    broadcast = InlineKeyboardButton(
        text="Создать рассылку", callback_data="create_broadcast"
    )

    users_moderation = InlineKeyboardButton(
        text="Управление пользователями", callback_data="users_moderation"
    )

    ads_moderation = InlineKeyboardButton(
        text="Управление объявлениями", callback_data="ads_moderation"
    )

    to_admin_panel = InlineKeyboardButton(
        text="К панели администратора", callback_data="to_admin_panel"
    )


class AdminMainKeyboards:

    main_window = InlineKeyboardMarkup(
            inline_keyboard=[
                *AdminMainButtons.main_window_buttons,
                [AdminMainButtons.administer]
            ]
    )

    admin_panel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                AdminMainButtons.broadcast
            ],
            [
                AdminMainButtons.statistic
            ],
            [
                AdminMainButtons.users_moderation
            ],
            [
                AdminMainButtons.ads_moderation
            ],
            [
                GeneralButtons.to_main_menu
            ]
        ]
    )

    to_admin_panel = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                AdminMainButtons.to_admin_panel,
            ]
        ]
    )
