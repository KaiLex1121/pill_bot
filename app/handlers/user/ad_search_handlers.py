from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.storage.redis import Redis

from app.states.user import AdSearchStates
from app.keyboards.user import AdSearchKeyboards
from app.text.user import AdSearchText
from app.dao.holder import HolderDAO
from app.filters import AdTypeFilter
from app.models.dto import User
from app.states.user import AdCreationStates

router: Router = Router()



@router.callback_query(F.data == "to_current_handler")
async def return_to_current_handler(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == AdSearchStates.FILL_CITY:
        await fill_ad_type(callback, state)
    elif current_state == AdSearchStates.FILL_DRUGS:
        await fill_city(callback, state)


@router.callback_query(
    F.data == "find_ads",
    StateFilter(AdCreationStates.ADS_WINDOW),
)
async def fill_ad_type(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(
            text="Выбери тип объявления. Ты хочешь посмотреть объявления тех, кто ищет лекарства, отдает их или все объявления",
            reply_markup=AdSearchKeyboards.fill_ad_type
        )
    except TelegramBadRequest:
        pass
    await state.set_state(AdSearchStates.FILL_CITY)


@router.callback_query(
    StateFilter(AdSearchStates.FILL_CITY),
    AdTypeFilter()
)
async def fill_city(
    callback: CallbackQuery,
    state: FSMContext,
):
    message_to_delete = await callback.message.edit_text(
        text="Введи город, в котором хочешь найти   лекарство. Или укажи ближайший крупный - это увеличит количество объявлений",
        reply_markup=AdSearchKeyboards.to_main_menu
    )
    if callback.data != "to_current_handler":
        await state.update_data(
            {
                'message_to_delete': message_to_delete.message_id,
                'ad_type': callback.data
            }
        )

    await state.set_state(AdSearchStates.FILL_DRUGS)


@router.message(
    StateFilter(AdSearchStates.FILL_DRUGS),
    F.text
)
async def fill_drugs(message: Message, state: FSMContext, bot: Bot):
    dct = await state.get_data()
    await bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=dct['message_to_delete']
    )
    message_to_delete = await message.answer(
        text="Введи действующее вещество или название лекарства",
        reply_markup=AdSearchKeyboards.to_main_menu
    )

    await state.update_data(
        {
            'city': message.text,
            'message_to_delete': message_to_delete.message_id
        }
    )
    await state.set_state(AdSearchStates.CONFIRM_AD_SEARCH)


@router.message(
    StateFilter(AdSearchStates.CONFIRM_AD_SEARCH),
    F.text
)
async def confirm_ad_search(message: Message, state: FSMContext, bot: Bot):
    dct = await state.get_data()
    await state.update_data(
        {
            'drugs': message.text,
        }
    )
    await bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=dct['message_to_delete']
    )
    await message.answer(
        text=AdSearchText.show_search_preview(
            city=dct['city'],
            drugs=message.text
        ),
        reply_markup=AdSearchKeyboards.find_ads
    )


@router.callback_query(
    F.data == "show_next_ad"
)
@router.callback_query(
    F.data == "confirm_and_find_ads"
)
async def show_next_ad(
    callback: CallbackQuery,
    state: FSMContext,
    redis: Redis,
    dao: HolderDAO
):
    dct = await state.get_data()
    offset_key = f"user:{callback.from_user.id}:user_offset"
    current_offset = await redis.get(offset_key)
    current_offset = int(current_offset) if current_offset else 0

    ad = await dao.advertisment.get_required_ads_by_limit(
        ad_type=dct['ad_type'],
        city=dct['city'],
        drugs=dct['drugs'],
        offset_=current_offset,
        limit_=1,
    )
    if ad:
        await redis.set(offset_key, current_offset + 1)
        await callback.message.answer(
            text=AdSearchText.show_ad_text(ad),
            reply_markup=AdSearchKeyboards.ad_window
        )
    else:
        await redis.set(offset_key, 0)
        await callback.message.answer(
            text=f"Объявления закончились. Для выхода нажмите «В главное меню»",
            reply_markup=AdSearchKeyboards.to_main_menu
        )
    await callback.message.delete_reply_markup()

    await state.update_data(
        {
            'ad_id': ad.id
        }
    )


@router.callback_query(
    F.data == "add_to_favorite"
)
async def append_ad_to_favorites(
    callback: CallbackQuery,
    state: FSMContext,
    dao: HolderDAO,
    user: User
):
    dct = await state.get_data()
    ad = await dao.advertisment.get_by_id(dct['ad_id'])
    user = await dao.user.get_by_id(user.db_id)
    user.favorite_advertisements.append(ad)
    await dao.commit()
    await callback.answer(
        text="Объявление добавлено в Избранные"
    )

@router.callback_query(
    F.data == "cancel_ad_search"
)
async def cancel_ad_search(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=AdSearchText.cancel_ad_search,
        reply_markup=AdSearchKeyboards.confirm_returning
    )


@router.callback_query(
    F.data == "cancel_ad_search_filling"
)
async def cancel_ad_search_filling(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=AdSearchText.cancel_ad_search,
        reply_markup=AdSearchKeyboards.confirm_returning
    )
