from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from app.dao import HolderDAO
from app.models.dto import User
from app.services.general import send_message_safely
from app.handlers.user.main_handlers import show_user_ads
from app.text.user import AdSearchText


router: Router = Router()


@router.callback_query(
    F.data == 'show_created_ads'
)
async def show_created_ads(
    callback: CallbackQuery,
    bot: Bot,
    user: User,
    dao: HolderDAO
):
    list_of_ads = await dao.user.get_all_user_ads_by_id(user.db_id)
    await callback.message.answer(
        text="Созданные тобой объявления:"
    )
    for ad in list_of_ads:
        await send_message_safely(
            bot,
            user.tg_id,
            AdSearchText.show_ad_text(ad)
        )
    await show_user_ads(callback)


@router.callback_query(
    F.data == 'show_favorite_ads'
)
async def show_favorite_ads(
    callback: CallbackQuery,
    bot: Bot,
    dao: HolderDAO,
    user: User
):
    user = await dao.user.get_by_id(user.db_id)
    list_of_ads = user.favorite_advertisements
    await callback.message.answer(
        text="Объявления, добавленные в избранное:"
    )
    for ad in list_of_ads:
        await send_message_safely(
            bot,
            user.tg_id,
            AdSearchText.show_ad_text(ad),
        )

    await show_user_ads(callback)