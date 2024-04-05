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


router: Router = Router()


@router.callback_query(
    F.data == 'find_ads'
)
async def fill_city(callback: CallbackQuery, state: FSMContext):
    message_to_delete = await callback.message.edit_text(
        text="Введи город, в котором хочешь найти лекарство. Или укажи \
            ближайший крупный - это увеличит количество объявлений",
        reply_markup=AdSearchKeyboards.to_main_menu
    )
    await state.update_data(
        {
            'message_to_delete': message_to_delete.message_id
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
        text="Введи действующее вещество или название лекарства, которое хочешь найти",
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


@router.callback_query(
    F.data == "cancel_ad_search"
)
async def cancel_ad_search(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=AdSearchText.cancel_ad_search,
        reply_markup=AdSearchKeyboards.confirm_returning
    )
