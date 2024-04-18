from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from app.dao.holder import HolderDAO
from app.services.general import broadcast
from app.filters import admin_filters
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
