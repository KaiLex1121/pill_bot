from asyncio import create_task, sleep

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter, or_f, and_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from .genereal_handlers import general_back_to_main_menu
from app.services.user import find_message_to_delete
from app.states.user import AdCreationStates
from app.keyboards.user import AdCreationKeyboards
from app.text.user import AdCreationText
from app.dao.holder import HolderDAO
from app.filters import AdTypeFilter, DeliveryTypeFilter
from app.enums.advertisment import TypeOfDelivery, TypeOfAd
from app.models.dto.user import User

router: Router = Router()


@router.callback_query(F.data == "create_ad")
async def create_ad(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Выбери тип объявления. Ищешь лекарство или хочешь отдать",
        reply_markup=AdCreationKeyboards.fill_ad_type
    )
    await state.set_state(AdCreationStates.FILL_ADD_TYPE)


@router.callback_query(
    StateFilter(AdCreationStates.FILL_ADD_TYPE),
    AdTypeFilter()
)
async def fill_ad_type(
    callback: CallbackQuery,
    state: FSMContext,
    ad_type_enum: TypeOfAd
):
    message_to_delete = await callback.message.edit_text(
        text="Укажи свой или ближайший крупный город, это повысит шансы быть найденным",
        reply_markup=AdCreationKeyboards.to_main_menu
    )
    await state.update_data(
        {
            'ad_type': ad_type_enum.value,
            'message_to_delete': message_to_delete.message_id
        }
    )
    await state.set_state(AdCreationStates.FILL_CITY)


@router.message(
    StateFilter(AdCreationStates.FILL_CITY),
    F.text,
)
async def fill_city(message: Message, state: FSMContext, bot: Bot):
    next_message_to_delete = await message.answer(
        text="Добавь лекарства, которые хочешь найти или отдать",
        reply_markup=AdCreationKeyboards.to_main_menu
    )
    try:
        current_message_to_delete = await find_message_to_delete(state)
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=current_message_to_delete
        )
    except TelegramBadRequest:
        await message.delete()
    await state.set_state(AdCreationStates.FILL_DRUGS)

    if message.text != AdCreationText.cancel_ad_creating:
        await state.update_data(
            {
                'city': message.text,
                'message_to_delete': next_message_to_delete.message_id
            }
        )

# РАЗОБРАТЬСЯ ПОЧЕМУ ТУТ НЕ СРАБАТЫВАЕТ УДАЛЕНИЕ СООБЩЕНИЯ ИЗ ИЗ fill_city
@router.message(
    StateFilter(AdCreationStates.FILL_DRUGS),
    F.text
)
async def fill_drugs(message: Message, state: FSMContext, bot: Bot):
    await message.answer(
        text="Выбери, как хочешь получить или отдать лекарства",
        reply_markup=AdCreationKeyboards.fill_delivery_type
    )
    try:
        current_message_to_delete = await find_message_to_delete(state)
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=current_message_to_delete
        )
    except TelegramBadRequest:
        await message.delete()
    if message.text != AdCreationText.cancel_ad_creating:
        await state.update_data(
            {
                'drugs': message.text,
            }
        )
    await state.set_state(AdCreationStates.FILL_DELIVERY_TYPE)


@router.callback_query(
        StateFilter(AdCreationStates.FILL_DELIVERY_TYPE),
        DeliveryTypeFilter()
)
async def fill_delivery_type(
    callback: CallbackQuery,
    state: FSMContext,
    delivery_type_enum: TypeOfDelivery
):
    message_to_delete = await callback.message.edit_text(
        text="Укажи что-то еще, что считаешь нужным",
        reply_markup=AdCreationKeyboards.to_main_menu
    )
    await state.update_data(
        {
            'delivery_type': delivery_type_enum.value,
            'message_to_delete': message_to_delete.message_id
        }
    )
    await state.set_state(AdCreationStates.FILL_ADDITIONAL_TEXT)


@router.message(
    StateFilter(AdCreationStates.FILL_ADDITIONAL_TEXT),
    F.text
)
async def fill_additional_text(message: Message, state: FSMContext, bot: Bot):
    try:
        current_message_to_delete = await find_message_to_delete(state)
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=current_message_to_delete
        )
    except TelegramBadRequest:
        await message.delete()
    next_message_to_delete = await message.answer(
        text="Создание анкеты завершено. Показать ее?",
        reply_markup=AdCreationKeyboards.show_ad_preview
    )
    if message.text != AdCreationText.cancel_ad_creating:
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
    dct = await state.get_data()
    await callback.message.edit_text(
        text=AdCreationText.show_ad_preview(
            ad_type=dct['ad_type'],
            city=dct['city'],
            drugs=dct['drugs'],
            delivery_type=dct['delivery_type'],
            additional_text=dct['additional_text'],
            username=callback.from_user.username
        ),
        reply_markup=AdCreationKeyboards.confirm_ad_creation
    )
    await state.set_state(AdCreationStates.CONFIRM_AD_CREATION)


@router.callback_query(
    StateFilter(AdCreationStates.CONFIRM_AD_CREATION),
    F.data == "confirm_ad_creation"
)
async def confirm_ad_creation(
    callback: CallbackQuery,
    state: FSMContext,
    dao: HolderDAO,
    user: User
):
    fsm_dict = await state.get_data()
    await dao.advertisment.create_ad(
        user_id=user.db_id,
        FSM_dict=fsm_dict
    )
    await callback.message.answer(
        text="Объявление сохраненно. Вы можете взаимодействовать с ним тут: Главное меню > Профиль > Мои бъявления > Созданные > выбираете нужное"
    )
    await general_back_to_main_menu(callback, state)


@router.callback_query(
    F.data == "cancel_ad_creation"
)
async def cancel_ad_creation(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=AdCreationText.cancel_ad_creating,
        reply_markup=AdCreationKeyboards.confirm_returning
    )



# @router.callback_query(
#     F.data == "to_current_handler",
#     AdTypeFilter()

# )
# async def return_to_current_handler(
#     callback: CallbackQuery,
#     state: FSMContext,
#     bot: Bot,
#     ad_type_enum
# ):

#     if await state.get_state() == AdCreationStates.FILL_ADD_TYPE:
#         await create_ad(callback, state)

#     elif await state.get_state() == AdCreationStates.FILL_CITY:
#         await fill_ad_type(callback, state, ad_type_enum)

#     elif await state.get_state() == AdCreationStates.FILL_DRUGS:
#         await fill_city(callback.message, state, bot)

#     elif await state.get_state() == AdCreationStates.FILL_DELIVERY_TYPE:
#         await fill_drugs(callback.message, state, bot)

#     elif await state.get_state() == AdCreationStates.FILL_ADDITIONAL_TEXT:
#         await fill_delivery_type(callback, state, ad_type_enum)

#     elif await state.get_state() == AdCreationStates.SHOW_AD_PREVIEW:
#         await fill_additional_text(callback.message, state, bot)

#     else:
#         await show_ad_preview(callback, state)
