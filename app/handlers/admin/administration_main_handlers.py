from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from app.services.general import broadcast
from app.keyboards.admin import AdminMainKeyboards


router: Router = Router()


@router.callback_query(
    F.data == "administer_bot",
)
async def show_admin_panel(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Панель админитстратора",
        reply_markup=AdminMainKeyboards.admin_panel
    )


@router.callback_query(
    F.data == "to_admin_panel",
)
async def to_admin_panel(callback: CallbackQuery, state: FSMContext):
    await show_admin_panel(callback, state)
