from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from app.states.user import MainStates
from app.states.user import FeedbackCreationStates, AdCreationStates
from app.keyboards.user import MainKeyboards, GeneralKeyboards
from app.text.user import OnboardingText, MainText
from app.dao import HolderDAO


router: Router = Router()


@router.callback_query(
    F.data == 'show_created_ads'
)
async def show_created_ads(callback: CallbackQuery, user, dao: HolderDAO):
    res = await dao.user.get_all_user_ads_by_id(user.tg_id)

    for res in res:
        print(res.__dict__)

    await callback.message.edit_text(
        text="Созданные объявленияㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
        reply_markup=MainKeyboards.profile_window
    )


@router.callback_query(
    F.data == 'show_like_ads'
)
async def show_liked_ads(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Лайкнутые объявленияㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
        reply_markup=MainKeyboards.profile_window
    )
