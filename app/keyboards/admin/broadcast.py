from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class AdminButtons:

    get_back_button = InlineKeyboardButton(
        text="Назад", callback_data="get_back_button_pressed"
    )

    make_broadcast_button = InlineKeyboardButton(
        text="Создать рассылку",
        callback_data="create_broadcast_button_pressed"
    )

    cancel_broadcast_button = InlineKeyboardButton(
        text="❌ ОТМЕНИТЬ ❌",
        callback_data="cancel_broadcast_button_pressed"
    )

    confirm_broadcast_button = InlineKeyboardButton(
        text="✅ ОТПРАВИТЬ ✅",
        callback_data="confirm_broadcast_button_pressed"
    )

    get_statistic_button = InlineKeyboardButton(
        text="Статистика",
        callback_data="get_statistic_button_pressed"
    )

    users_count_button = InlineKeyboardButton(
        text="Количество всех пользователей",
        callback_data="users_count_button_pressed"
    )

    last_seven_days_uers_count_button = InlineKeyboardButton(
        text="Пользователи за последние 7 дней",
        callback_data="last_seven_days_button_pressed"
    )


class AdminKeyboards:

    initial_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                AdminButtons.make_broadcast_button
            ],
        ]
    )

    broadcast_preview_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                AdminButtons.confirm_broadcast_button,
                AdminButtons.cancel_broadcast_button

            ],
        ]
    )
