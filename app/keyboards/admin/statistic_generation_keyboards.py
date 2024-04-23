from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.keyboards.admin import AdminMainButtons


class StatisticGenerationButtons:

    to_statistic_generation_window = InlineKeyboardButton(
        text="Назад", callback_data="to_statistic_generation_window"
    )

    get_all_users_count = InlineKeyboardButton(
        text="Количество всех пользователей",
        callback_data="get_users_count"
    )

    get_new_users_count_for_yesterday = InlineKeyboardButton(
        text="Новые за вчера",
        callback_data="get_new_users_count_for_yesterday"
    )

    get_active_users_count_for_yesterday = InlineKeyboardButton(
        text="Активные за вчера",
        callback_data="get_active_users_count_for_yesterday"
    )


class StatisticGenerationKeyboards:

    statistic_generation = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                StatisticGenerationButtons.get_all_users_count,
            ],
            [
                StatisticGenerationButtons.get_new_users_count_for_yesterday,
                StatisticGenerationButtons.get_active_users_count_for_yesterday
            ],
            [
                AdminMainButtons.to_admin_panel
            ]
        ]
    )
