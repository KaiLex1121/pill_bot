from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from app.states.user.main_states import MainDialogStates
from app.text.user.main_text import MainDialogText
from app.keyboards.user.main_keyboards import MainKeyboards


router: Router = Router()


@router.callback_query(
    F.data == 'to_main_menu'
)
async def general_back_to_menu(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer(
            text=MainDialogText.main_window,
            reply_markup=MainKeyboards.main_window
        )
    await callback.message.delete()
    await state.set_state(MainDialogStates.MAIN_DIALOG)
