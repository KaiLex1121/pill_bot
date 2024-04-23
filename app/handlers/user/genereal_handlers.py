from asyncio import sleep

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from app.keyboards.admin import AdminMainKeyboards
from app.models.dto import User
from app.states.user import MainStates
from app.text.user import MainText
from app.keyboards.user import MainKeyboards


router: Router = Router()


@router.callback_query(
    F.data == 'to_main_menu',
)
async def general_back_to_main_menu(
    callback: CallbackQuery,
    state: FSMContext,
    user: User
):
    try:
        await callback.message.edit_reply_markup()
    except TelegramBadRequest:
        pass
    if user.is_admin:
        keyboard = AdminMainKeyboards.main_window
    else:
        keyboard = MainKeyboards.main_window
    await callback.message.edit_text(
            text=MainText.main_window,
            reply_markup=keyboard
        )
    await state.set_state(MainStates.MAIN_DIALOG)


@router.message(
    Command("main_menu")
)
async def genereal_to_main_menu(
    message: Message,
    state: FSMContext,
    user: User
):
    if user.is_admin:
        keyboard = AdminMainKeyboards.main_window
    else:
        keyboard = MainKeyboards.main_window
    await state.set_state(MainStates.MAIN_DIALOG)
    try:
        await message.edit_reply_markup()
        await message.edit_text(
            text=MainText.main_window,
            reply_markup=keyboard
        )
    except TelegramBadRequest:
        await message.answer(
            text=MainText.main_window,
            reply_markup=keyboard
        )