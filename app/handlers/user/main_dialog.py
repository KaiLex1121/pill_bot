from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from app.states.user.main_states import MainDialogStates
from app.keyboards.user.main_keyboards import MainKeyboards
from app.dao.holder import HolderDAO
from app.models import dto
from app.text.user.onboarding_text import OnboardingText
from app.text.user.main_text import MainDialogText

router: Router = Router()
router.message.filter(StateFilter(MainDialogStates.MAIN_DIALOG))


@router.callback_query(
    F.data == 'rules_accepted'
)
async def show_main_window(callback: CallbackQuery):
    try:
        await callback.message.delete_reply_markup()
    except TelegramBadRequest:
        pass
    await callback.message.answer(
        text=MainDialogText.main_window,
        reply_markup=MainKeyboards.main_window
    )


@router.callback_query(
    F.data == 'show_ads'
)
async def ads(callback: CallbackQuery,):
    await callback.message.edit_text(
        text=MainDialogText.ads_window,
        reply_markup=MainKeyboards.ads_window
    )


@router.callback_query(
    F.data == 'show_profile'
)
async def show_profile(callback: CallbackQuery):
    await callback.message.edit_text(
        text=MainDialogText.profile_window,
        reply_markup=MainKeyboards.profile_window
    )

@router.callback_query(
    F.data == 'show_user_ads'
)
async def show_user_ads(callback: CallbackQuery):
    await callback.message.edit_text(
        text=MainDialogText.user_ads_window,
        reply_markup=MainKeyboards.show_user_ads
    )


@router.callback_query(
    F.data == 'show_created_ads'
)
async def show_created_ads(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Созданные объявленияㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
        reply_markup=MainKeyboards.profile_window
    )


@router.callback_query(
    F.data == 'show_like_ads'
)
async def show_liked_ads(callback: CallbackQuery):
    await callback.message.answer(
        text="Лайкнутые объявленияㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
        reply_markup=MainKeyboards.profile_window
    )



@router.callback_query(
    F.data == 'show_rules'
)
async def show_rules(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text=OnboardingText.rules_one,
        reply_markup=MainKeyboards.show_rules
    )


@router.callback_query(
    F.data == 'show_second_rules'
)
async def show_second_rules(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        text=OnboardingText.rules_two,
        reply_markup=MainKeyboards.show_second_rules
    )

@router.callback_query(
    F.data == 'to_main_menu'
)
async def back_to_menu(callback: CallbackQuery):
    await callback.message.delete()
    await show_main_window(callback)



@router.message()
async def message_echo(message: Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(
        text=f"Message попал сюда c состоянием {state}"
    )


@router.callback_query()
async def callback_echo(callback: CallbackQuery, state: FSMContext):
    state = await state.get_state()
    await callback.message.answer(
        text=f"Callback попал сюда c состоянием {state}"
    )