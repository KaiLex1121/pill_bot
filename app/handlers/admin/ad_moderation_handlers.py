from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


from app.dao.holder import HolderDAO
from app.filters import AdModerationCallbackFilter
from app.keyboards.admin import AdModerationKeyboards


router: Router = Router()


@router.callback_query(
    AdModerationCallbackFilter.filter(F.callback_data == "ad_moderation")
)
async def show_moderation_panel(
    callback: CallbackQuery,
    callback_data: AdModerationCallbackFilter,
    state: FSMContext
):
    await state.update_data(
        {
            'ad_owner_id': callback_data.ad_owner_id,
            'ad_id': callback_data.ad_id
        }
    )
    await callback.message.edit_text(
        text=callback.message.text,
        reply_markup=AdModerationKeyboards.moderation_panel
    )


@router.callback_query(
    F.data == "hide_ad",
)
async def hide_ad(
    callback: CallbackQuery,
    state: FSMContext,
    dao: HolderDAO,
):
    dct = await state.get_data()
    ad_id = dct['ad_id']
    await dao.advertisment.hide_ad_by_id(ad_id)
    await callback.answer(
        text="Объявление удалено из выдачи",
        reply_markup=callback.message.reply_markup
    )


@router.callback_query(
    F.data == "unhide_ad",
)
async def unhide_ad(
    callback: CallbackQuery,
    state: FSMContext,
    dao: HolderDAO,
):
    dct = await state.get_data()
    ad_id = dct['ad_id']
    await dao.advertisment.unhide_ad_by_id(ad_id)
    await callback.answer(
        text="Объявление добавлено обратно",
        reply_markup=callback.message.reply_markup
    )


@router.callback_query(
    F.data == "ban_ad_owner",
)
async def ban_ad_owner(
    callback: CallbackQuery,
    state: FSMContext,
    dao: HolderDAO,
):
    dct = await state.get_data()
    ad_owner_id = dct['ad_owner_id']
    await dao.user.ban_user_by_db_id(ad_owner_id)
    await callback.answer(
        text="Пользователь забанен",
        reply_markup=callback.message.reply_markup
    )


@router.callback_query(
    F.data == "unban_ad_owner",
)
async def unban_ad_owner(
    callback: CallbackQuery,
    state: FSMContext,
    dao: HolderDAO,
):
    dct = await state.get_data()
    ad_owner_id = dct['ad_owner_id']
    await dao.user.unban_user_by_db_id(ad_owner_id)
    await callback.answer(
        text="Пользователь разбанен",
        reply_markup=callback.message.reply_markup
    )
