from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from .genereal_handlers import general_back_to_main_menu
from app.services.user import find_message_to_delete
from app.services.admin import create_ad_moderation_keyboard
from app.states.user import AdCreationStates
from app.keyboards.user import AdCreationKeyboards
from app.text.user import AdCreationText
from app.dao.holder import HolderDAO
from app.filters import AdTypeFilter, DeliveryTypeFilter
from app.models.dto.user import User


router: Router = Router()


@router.callback_query(
    F.data == "to_current_creation_handler",
)
async def return_to_current_handler(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot,
):
    current_state = await state.get_state()
    if current_state == AdCreationStates.FILL_CITY:
        await fill_ad_type(callback, state)
    elif current_state == AdCreationStates.FILL_DRUGS:
        await fill_city(callback, state)
    elif current_state == AdCreationStates.FILL_DELIVERY_TYPE:
        await fill_drugs(callback.message, state, bot)
    elif current_state == AdCreationStates.FILL_ADDITIONAL_TEXT:
        await fill_delivery_type(callback.message, state, bot)
    elif current_state == AdCreationStates.SHOW_AD_PREVIEW:
        await fill_additional_text(callback, state)
    elif current_state == AdCreationStates.CONFIRM_AD_CREATION:
        await show_ad_preview(callback.message, state, bot)


@router.callback_query(F.data == "create_ad")
async def fill_ad_type(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Выбери тип объявления. Хочешь найти таблетки или отдать",
        reply_markup=AdCreationKeyboards.fill_ad_type
    )
    await state.set_state(AdCreationStates.FILL_CITY)


@router.callback_query(
    StateFilter(AdCreationStates.FILL_CITY),
    AdTypeFilter()
)
async def fill_city(
    callback: CallbackQuery,
    state: FSMContext,
):
    message_to_delete = await callback.message.edit_text(
        text="Укажи свой или ближайший крупный город, чтобы твое объявление было легче найти",
        reply_markup=AdCreationKeyboards.to_main_menu
    )
    if callback.data != "to_current_creation_handler":
        await state.update_data(
            {
                'ad_type': callback.data,
                'message_to_delete': message_to_delete.message_id
            }
        )
    await state.set_state(AdCreationStates.FILL_DRUGS)


@router.message(
    StateFilter(AdCreationStates.FILL_DRUGS),
    F.text,
)
async def fill_drugs(message: Message, state: FSMContext, bot: Bot):

    current_message_to_delete = await find_message_to_delete(state)

    if message.text != AdCreationText.cancel_ad_creating:
        message_to_delete = await message.answer(
            text="Добавь лекарства, которые хочешь найти или отдать",
            reply_markup=AdCreationKeyboards.to_main_menu
        )
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=current_message_to_delete
        )
        await state.update_data(
            {
                'city': message.text,
                'message_to_delete': message_to_delete.message_id
            }
        )
    else:
        await message.edit_text(
            text="Добавь лекарства, которые хочешь найти или отдать",
            reply_markup=AdCreationKeyboards.to_main_menu
        )

    await state.set_state(AdCreationStates.FILL_DELIVERY_TYPE)


@router.message(
    StateFilter(AdCreationStates.FILL_DELIVERY_TYPE),
    F.text
)
async def fill_delivery_type(message: Message, state: FSMContext, bot: Bot):
    current_message_to_delete = await find_message_to_delete(state)

    if message.text != AdCreationText.cancel_ad_creating:
        await message.answer(
            text="Выбери, как хочешь получить или отдать лекарства",
            reply_markup=AdCreationKeyboards.fill_delivery_type
        )
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=current_message_to_delete
        )
        await state.update_data(
            {
                'drugs': message.text,
            }
        )
    else:
        await message.edit_text(
            text="Выбери, как хочешь получить или отдать лекарства",
            reply_markup=AdCreationKeyboards.fill_delivery_type
        )
    await state.set_state(AdCreationStates.FILL_ADDITIONAL_TEXT)


@router.callback_query(
        StateFilter(AdCreationStates.FILL_ADDITIONAL_TEXT),
        DeliveryTypeFilter()
)
async def fill_additional_text(
    callback: CallbackQuery,
    state: FSMContext,
):
    message_to_delete = await callback.message.edit_text(
        text="Укажи что-то еще, что считаешь нужным",
        reply_markup=AdCreationKeyboards.to_main_menu
    )
    if callback.data != "to_current_creation_handler":
        await state.update_data(
            {
                'delivery_type': callback.data,
                'message_to_delete': message_to_delete.message_id
            }
        )
    await state.set_state(AdCreationStates.SHOW_AD_PREVIEW)


@router.message(
    StateFilter(AdCreationStates.SHOW_AD_PREVIEW),
    F.text
)
async def show_ad_preview(message: Message, state: FSMContext, bot: Bot):
    fsm_storage = await state.get_data()
    if message.text.strip() != AdCreationText.cancel_ad_creating:
        additional_text = message.text
        ad_text = AdCreationText.show_ad_preview(
                    ad_type=fsm_storage['ad_type'],
                    city=fsm_storage['city'],
                    drugs=fsm_storage['drugs'],
                    delivery_type=fsm_storage['delivery_type'],
                    additional_text=additional_text,
                    username=message.from_user.username
                )
        await state.update_data(
            {   'additional_text': additional_text,
                'ad_text': ad_text
            }
        )
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=fsm_storage['message_to_delete']
        )
        await message.answer(
            text=ad_text,
            reply_markup=AdCreationKeyboards.confirm_ad_creation
        )
    else:
        await message.edit_text(
            text=fsm_storage['ad_text'],
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
    user: User,
    bot: Bot
):
    fsm_storage = await state.get_data()
    ad_text = fsm_storage['ad_text']
    created_ad = await dao.advertisment.create_ad(
        user_id=user.db_id,
        FSM_dict=fsm_storage
    )
    ad_moderation_keyboard = create_ad_moderation_keyboard(
        ad_id=created_ad.id,
        ad_owner_id=user.db_id
    )
    await bot.send_message(
        chat_id=-4144959991,
        text=ad_text,
        reply_markup=ad_moderation_keyboard
    )
    await callback.message.answer(
        text="Объявление сохраненно. Вы можете взаимодействовать с ним тут: Главное меню > Профиль > Мои бъявления > Созданные > выбираете нужное"
    )
    await general_back_to_main_menu(callback, state, user)


@router.callback_query(
    F.data == "cancel_ad_creation"
)
async def cancel_ad_creation(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=AdCreationText.cancel_ad_creating,
        reply_markup=AdCreationKeyboards.confirm_returning
    )
