from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.services.message_finder import find_message_to_delete
from app.states.user.ad_creation_states import AdCreationStates
from app.keyboards.user.ad_creation_keyboards import AdCreationKeyboards

from app.dao.holder import HolderDAO
from app.models import dto


router: Router = Router()


@router.callback_query(F.data == "create_ad")
async def create_ad(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        text="Выбери тип объявления. Ищешь лекарство или хочешь отдать",
        reply_markup=AdCreationKeyboards.fill_ad_type
    )
    await state.set_state(AdCreationStates.FILL_ADD_TYPE)


@router.callback_query(StateFilter(AdCreationStates.FILL_ADD_TYPE))
@router.callback_query(F.data == "take")
@router.callback_query(F.data == "give")
async def fill_ad_type(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    message_to_delete = await callback.message.answer(
        text="Укажи свой или ближайший крупный город, это повысит шансы быть найденным",
        reply_markup=AdCreationKeyboards.to_main_menu,
    )
    await state.update_data(
        {
            'ad_type': callback.data,
            'message_to_delete': message_to_delete.message_id,
        }
    )
    await state.set_state(AdCreationStates.FILL_CITY)


@router.message(
    StateFilter(AdCreationStates.FILL_CITY),
    F.text,
)
async def fill_city(message: Message, state: FSMContext, bot: Bot):
    current_message_to_delete = await find_message_to_delete(state)
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=current_message_to_delete
    )

    next_message_to_delete = await message.answer(
        text="Добавь лекарства, которые хочешь найти или отдать",
        reply_markup=AdCreationKeyboards.to_main_menu
    )
    await state.update_data(
        {
            'city': message.text,
            'message_to_delete': next_message_to_delete.message_id
        }
    )
    await state.set_state(AdCreationStates.FILL_DRUGS)


@router.message(
    StateFilter(AdCreationStates.FILL_DRUGS),
    F.text
)
async def fill_drugs(message: Message, state: FSMContext, bot: Bot):
    current_message_to_delete = await find_message_to_delete(state)
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=current_message_to_delete
    )
    await message.answer(
        text="Выбери, как хочешь получить или отдать лекарства",
        reply_markup=AdCreationKeyboards.fill_delivery_type
    )
    await state.update_data(
        {
            'drugs': message.text,
        }
    )
    await state.set_state(AdCreationStates.FILL_DELIVERY_TYPE)


@router.callback_query(StateFilter(AdCreationStates.FILL_ADD_TYPE))
@router.callback_query(F.data == "meeting")
@router.callback_query(F.data == "delivery")
async def fill_delivery_type(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    message_to_delete = await callback.message.answer(
        text="Укажи что-то еще, что считаешь нужным",
        reply_markup=AdCreationKeyboards.to_main_menu
    )
    await state.update_data(
        {
            'delivery_type': callback.data,
            'message_to_delete': message_to_delete.message_id
        }
    )
    await state.set_state(AdCreationStates.FILL_ADDITIONAL_TEXT)


@router.message(
    StateFilter(AdCreationStates.FILL_ADDITIONAL_TEXT),
    F.text
)
async def fill_additional_text(message: Message, state: FSMContext, bot: Bot):
    current_message_to_delete = await find_message_to_delete(state)
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=current_message_to_delete
    )

    next_message_to_delete = await message.answer(
        text="Создание анкеты завершено. Показать ее?",
        reply_markup=AdCreationKeyboards.show_ad_preview
    )
    await state.update_data(
        {
            'additional_text': message.text,
            'message_to_delete': next_message_to_delete.message_id
        }
    )
    await state.set_state(AdCreationStates.SHOW_AD_PREVIEW)


@router.callback_query(
    StateFilter(AdCreationStates.SHOW_AD_PREVIEW),
    F.data == "show_ad_preview"
)
async def show_ad_preview(callback: CallbackQuery, state: FSMContext):
    txt = await state.get_data()
    await callback.message.delete()
    await callback.message.answer(
        text=f"{txt}",
        reply_markup=AdCreationKeyboards.to_main_menu
    )
    await state.set_state(AdCreationStates.FILL_ADDITIONAL_TEXT)
