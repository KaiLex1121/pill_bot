from aiogram import Router, F, Bot
from aiogram.filters import Text, StateFilter
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.redis import Redis

from app.keyboards.inline_keyboards import InlineAdminKeyboards
from app.lexicon.messages import AdminMessages

from app.states.admin_states import MakeBroadcastState
from app.dao.holder import HolderDAO
from app.services.broadcaster import broadcast
from app.filters import admin_filters


router: Router = Router()
router.message.filter(admin_filters.AdminFilter())


async def message_echo(message: Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(text=f"Message попал сюда c состоянием {state}")


async def callback_echo(callback: CallbackQuery, state: FSMContext):
    state = await state.get_state()
    await callback.answer(text=f"Callback попал сюда c состоянием {state}")
