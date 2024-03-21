from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.user.main_states import MainDialogStates
from app.dao.holder import HolderDAO
from app.models import dto


router: Router = Router()
router.message.filter(StateFilter(MainDialogStates.MAIN_DIALOG))


@router.callback_query(
    F.data == 'rules_accepted'
)
async def show_main_window(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text="Главное меню"
    )


@router.message()
async def message_echo(message: Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(
        text=f"Message попал сюда c состоянием {state}"
    )


@router.callback_query()
async def callback_echo(callback: CallbackQuery, state: FSMContext):
    state = await state.get_state()
    await callback.message.answer(
        text=f"Callback попал сюда c состоянием {state}"
    )