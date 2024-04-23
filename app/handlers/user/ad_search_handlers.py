from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.storage.redis import Redis

from app.states.user import AdSearchStates
from app.keyboards.user import AdSearchKeyboards
from app.filters import AdTypeFilter
from app.text.user import AdSearchText
from app.dao.holder import HolderDAO
from app.models.dto import User
from app.services.admin import create_ad_moderation_keyboard


router: Router = Router()


@router.callback_query(
    F.data == "to_current_find_handler"
)
async def return_to_current_handler(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot,
    redis: Redis,
    dao: HolderDAO
):
    current_state = await state.get_state()
    if current_state == AdSearchStates.FILL_CITY:
        await fill_ad_type(callback, state)
    elif current_state == AdSearchStates.FILL_DRUGS:
        await fill_city(callback, state)
    elif current_state == AdSearchStates.CONFIRM_AD_SEARCH:
        await fill_drugs(callback.message, state, bot)
    elif current_state == AdSearchStates.SHOW_FOUND_ADS:
        await confirm_ad_search(callback.message, state, bot)
    elif current_state == AdSearchStates.SHOW_NEXT_AD:
        await show_next_ad(callback, state, redis, dao)


@router.callback_query(
    F.data == "find_ads",
)
async def fill_ad_type(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Выбери тип объявления. Ты хочешь посмотреть объявления тех, кто ищет лекарства, отдает их или все объявления",
        reply_markup=AdSearchKeyboards.fill_ad_type
    )
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
        text="Введи город, в котором хочешь найти лекарство. Или укажи ближайший крупный - это увеличит количество объявлений",
        reply_markup=AdSearchKeyboards.to_main_menu
    )

    if callback.data != "to_current_find_handler":
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
    if message.text.strip() != "Отменить поиск и вернуться в главное меню?":
        message_to_delete = await message.answer(
            text="Введи действующее вещество или название лекарства",
            reply_markup=AdSearchKeyboards.to_main_menu
        )
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=dct['message_to_delete']
        )
        await state.update_data(
            {
                'city': message.text,
                'message_to_delete': message_to_delete.message_id
            }
        )
    else:
        await message.edit_text(
            text="Введи действующее вещество или название лекарства",
            reply_markup=AdSearchKeyboards.to_main_menu
        )
    await state.set_state(AdSearchStates.CONFIRM_AD_SEARCH)


@router.message(
    StateFilter(AdSearchStates.CONFIRM_AD_SEARCH),
    F.text
)
async def confirm_ad_search(message: Message, state: FSMContext, bot: Bot):
    dct = await state.get_data()
    if message.text.strip() != "Отменить поиск и вернуться в главное меню?":
        await message.answer(
            text=AdSearchText.show_search_preview(
                city=dct['city'],
                drugs=message.text
            ),
            reply_markup=AdSearchKeyboards.find_ads
        )
        await bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=dct['message_to_delete']
        )
        await state.update_data(
            {
                'drugs': message.text,
            }
        )
    else:
        await message.edit_text(
            text=AdSearchText.show_search_preview(
                city=dct['city'],
                drugs=dct['drugs']
            ),
            reply_markup=AdSearchKeyboards.find_ads
        )
    await state.set_state(AdSearchStates.SHOW_FOUND_ADS)


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
    offset_key = f"user:{callback.from_user.id}:user_offset"

    if callback.data == "confirm_and_find_ads":
        await redis.set(offset_key, 0)

    current_offset = await redis.get(offset_key)
    current_offset = int(current_offset) if current_offset else 0

    dct = await state.get_data()

    ad = await dao.advertisment.get_required_ads_by_limit(
        ad_type=dct['ad_type'],
        city=dct['city'],
        drugs=dct['drugs'],
        offset_=current_offset,
        limit_=1,
    )

    if callback.data == "to_current_find_handler":
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            await callback.message.delete_reply_markup()
    else:
        await callback.message.delete_reply_markup()

    if ad:
        await redis.set(offset_key, current_offset + 1)
        await callback.message.answer(
            text=AdSearchText.show_ad_text(ad),
            reply_markup=AdSearchKeyboards.found_ad_window
        )
        await state.update_data(
            {
                'ad_id': ad.id,
                'ad_owner_id': ad.user.id
            }
        )
    elif not ad and callback.data == "confirm_and_find_ads":
        await callback.message.answer(
            text=f"Объявлений с такими параметрами нет. Для выхода нажми кнопку «В главное меню»",
            reply_markup=AdSearchKeyboards.to_main_menu
        )
    else:
        await callback.message.answer(
            text=f"Объявления закончились. Для выхода нажмите кнопку «В главное меню»",
            reply_markup=AdSearchKeyboards.to_main_menu
        )
    await state.set_state(AdSearchStates.SHOW_NEXT_AD)


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
    F.data == "report_ad"
)
async def report_ad(callback: CallbackQuery, state: FSMContext, bot: Bot):
    fsm_storage = await state.get_data()
    ad_moderation_keyboard = create_ad_moderation_keyboard(
        ad_id=fsm_storage['ad_id'],
        ad_owner_id=fsm_storage['ad_owner_id']
    )
    await bot.send_message(
            chat_id=-4164822207,
            text=callback.message.text,
            reply_markup=ad_moderation_keyboard
        )
    await callback.answer(
        text="Ваша жалоба отправлена. Спасибо!"
    )

@router.callback_query(
    F.data == "cancel_ad_search"
)
async def cancel_ad_search(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
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
