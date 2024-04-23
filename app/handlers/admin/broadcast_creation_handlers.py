from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.dao.holder import HolderDAO
from app.services.general import broadcast
from app.keyboards.admin import AdminMainKeyboards, BroadcastKeyboards
from app.states.admin import BroadcastCreatiionStates
from app.handlers.admin.administration_main_handlers import to_admin_panel


router: Router = Router()


@router.callback_query(
    F.data == "create_broadcast",
)
async def create_broadcast(
    callback: CallbackQuery,
    state: FSMContext,
):
    message_to_delete = await callback.message.edit_text(
        text="Пришли сообщение, которое хочешь отправить",
        reply_markup=AdminMainKeyboards.to_admin_panel
    )
    await state.set_data(
        {
            'message_to_delete': message_to_delete.message_id
        }
    )
    await state.set_state(BroadcastCreatiionStates.MESSAGE_ENTER)


@router.message(
    StateFilter(BroadcastCreatiionStates.MESSAGE_ENTER),
    F.text
)
async def show_broadcast_preview(
    message: Message,
    state: FSMContext,
    bot: Bot
):
    dct = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=dct['message_to_delete']
    )
    message_text = message.text
    await message.answer(
        text=f"Превью рассылки: «<i>{message_text}</i>»",
        reply_markup=BroadcastKeyboards.broadcast_preview_keyboard
    )

    await state.update_data({
        'broadcast_text': message_text
    })



@router.callback_query(
    F.data == "cancel_broadcast_sending",
)
async def cancel_broadcast_sending(
    callback: CallbackQuery,
    state: FSMContext,
):
    await callback.answer(
        text="Создание рассылки отменено"
    )
    await to_admin_panel(callback, state)



@router.callback_query(
    F.data == 'confirm_broadcast_sending'
)
async def confirm_broadcast_sending(
    callback: CallbackQuery,
    bot: Bot, state: FSMContext,
    dao: HolderDAO
):
    users = await dao.user.get_all()
    fsm_data = await state.get_data()
    broadcast_text = fsm_data['broadcast_text']
    await callback.message.edit_text(
        text='Идет отправка'
    )
    users_count = await broadcast(
        bot,
        users,
        text=broadcast_text
    )
    await callback.answer(
        text=f"Сообщение доставлено {users_count} пользователям",
    )
    await to_admin_panel(callback, state)