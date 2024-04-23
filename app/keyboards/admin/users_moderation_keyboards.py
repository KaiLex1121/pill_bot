from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.keyboards.admin import AdminMainButtons


class UsersModerationButtons:

    ban_user = InlineKeyboardButton(
        text="Заблокировать", callback_data="ban_user"
    )

    unban_user = InlineKeyboardButton(
        text="Разблокировать", callback_data="unban_user"
    )

    to_users_moderation = InlineKeyboardButton(
        text="К модерации пользователей", callback_data="to_users_moderation"
    )


class UsersModerationKeyboards:

    users_moderation = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                UsersModerationButtons.ban_user,
                UsersModerationButtons.unban_user
            ],
            [
                AdminMainButtons.to_admin_panel
            ]
        ]
    )

    to_users_moderation = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                UsersModerationButtons.to_users_moderation,
            ]
        ]
    )