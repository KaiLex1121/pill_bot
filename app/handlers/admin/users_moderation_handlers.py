from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.dao.holder import HolderDAO
from app.keyboards.admin import UsersModerationKeyboards
from app.states.admin import AdministrationMainStates


router: Router = Router()


@router.callback_query(
    F.data == "ban_user",
)
async def ban_user(
    callback: CallbackQuery,
    state: FSMContext,
):
    message_to_delete = await callback.message.edit_text(
        text="Введите имя пользователя, которого хотите заблокировать",
        reply_markup=UsersModerationKeyboards.to_users_moderation
    )
    await state.set_data(
        {
            'message_to_delete': message_to_delete.message_id
        }
    )
    await state.set_state(AdministrationMainStates.FILL_USERNAME_TO_BAN)


@router.message(
    StateFilter(AdministrationMainStates.FILL_USERNAME_TO_BAN),
    F.text
)
async def username_to_ban_filled(
    message: Message,
    dao: HolderDAO,
    state: FSMContext,
    bot: Bot
):
    dct = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=dct['message_to_delete']
    )
    username = message.text
    await dao.user.ban_user_by_username(username)
    await message.answer(
        text='Пользователь заблокирован',
        reply_markup=UsersModerationKeyboards.users_moderation
    )



@router.callback_query(
    F.data == "unban_user",
)
async def unban_user(
    callback: CallbackQuery,
    state: FSMContext,
):
    message_to_delete = await callback.message.edit_text(
        text="Введите имя пользователя, которого хотите разблокировать",
        reply_markup=UsersModerationKeyboards.to_users_moderation
    )
    await state.set_data(
        {
            'message_to_delete': message_to_delete.message_id
        }
    )
    await state.set_state(AdministrationMainStates.FILL_USERNAME_TO_UNBAN)


@router.message(
    StateFilter(AdministrationMainStates.FILL_USERNAME_TO_UNBAN),
    F.text
)
async def username_to_unban_filled(
    message: Message,
    dao: HolderDAO,
    state: FSMContext,
    bot: Bot
):
    dct = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=dct['message_to_delete']
    )
    username = message.text
    await dao.user.unban_user_by_username(username)
    await message.answer(
        text='Пользователь разблокирован',
        reply_markup=UsersModerationKeyboards.users_moderation
    )


@router.callback_query(
    F.data == "users_moderation",
)
async def moderate_users(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Управление пользователями бота",
        reply_markup=UsersModerationKeyboards.users_moderation
    )


@router.callback_query(
    F.data == "to_users_moderation",
)
async def to_users_moderation(callback: CallbackQuery, state: FSMContext):
    await moderate_users(callback, state)
