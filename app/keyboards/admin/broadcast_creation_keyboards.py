from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class BroadcastButtons:

    to_statistic_window = InlineKeyboardButton(
        text="Назад", callback_data="to_statistic_window"
    )

    cancel_broadcast = InlineKeyboardButton(
        text="Отменить рассылку",
        callback_data="cancel_broadcast_sending"
    )

    confirm_broadcast = InlineKeyboardButton(
        text="Отправить рассылку",
        callback_data="confirm_broadcast_sending"
    )


class BroadcastKeyboards:

    broadcast_preview_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                BroadcastButtons.confirm_broadcast,
                BroadcastButtons.cancel_broadcast,

            ],
        ]
    )
