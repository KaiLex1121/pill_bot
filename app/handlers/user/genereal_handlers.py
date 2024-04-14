from asyncio import sleep

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from app.states.user import MainStates
from app.text.user import MainText
from app.keyboards.user import MainKeyboards


router: Router = Router()


@router.callback_query(
    F.data == 'to_main_menu'
)
async def general_back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(
            text=MainText.main_window,
            reply_markup=MainKeyboards.main_window
        )
    await state.set_state(MainStates.MAIN_DIALOG)


@router.message(
    Command("main_menu")
)
async def genereal_to_main_menu(message: Message, state: FSMContext):

    try:
        await message.delete()
    except TelegramBadRequest:
        pass
    await message.answer(
            text=MainText.main_window,
            reply_markup=MainKeyboards.main_window
        )
    await state.set_state(MainStates.MAIN_DIALOG)
