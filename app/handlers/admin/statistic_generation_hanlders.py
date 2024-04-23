from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.dao.holder import HolderDAO
from app.keyboards.admin import StatisticGenerationKeyboards
from app.states.admin import BroadcastCreatiionStates
from app.handlers.admin.administration_main_handlers import to_admin_panel


router: Router = Router()


@router.callback_query(
    F.data == "get_statistic",
)
async def get_statistic(
    callback: CallbackQuery,
):
    await callback.message.edit_text(
        text="Выбери нужное",
        reply_markup=StatisticGenerationKeyboards.statistic_generation
    )


@router.callback_query(
    F.data == "get_users_count",
)
async def get_users_count(
    callback: CallbackQuery,
    dao: HolderDAO
):
    users_count = await dao.user.count()
    await callback.message.edit_text(
        text=f"Всего пользователей: {users_count}",
        reply_markup=callback.message.reply_markup
    )


@router.callback_query(
    F.data == "get_new_users_count_for_yesterday",
)
async def get_new_users_count_for_yesterday(
    callback: CallbackQuery,
    dao: HolderDAO
):
    users_count = await dao.user.get_required_users_count_for_required_day(
        days_ago=1,
        required_type='new_users'
    )
    try:
        await callback.message.edit_text(
            text=f"Новых пользователей за вчерашний день: {users_count}",
            reply_markup=callback.message.reply_markup
        )
    except TelegramBadRequest:
        pass

@router.callback_query(
    F.data == "get_active_users_count_for_yesterday",
)
async def get_active_users_count_for_yesterday(
    callback: CallbackQuery,
    dao: HolderDAO
):
    users_count = await dao.user.get_required_users_count_for_required_day(
        days_ago=1,
        required_type='active_users'
    )
    try:
        await callback.message.edit_text(
            text=f"Активных пользователей за вчерашний день: {users_count}",
            reply_markup=callback.message.reply_markup
        )
    except TelegramBadRequest:
        pass