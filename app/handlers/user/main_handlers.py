from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from app.states.user import MainStates
from app.states.user import FeedbackCreationStates, AdCreationStates
from app.keyboards.user import MainKeyboards, GeneralKeyboards
from app.keyboards.admin import AdminMainKeyboards
from app.text.user import OnboardingText, MainText
from app.models.dto import User

router: Router = Router()
router.message.filter(StateFilter(MainStates.MAIN_DIALOG))
router.callback_query.filter(StateFilter(MainStates.MAIN_DIALOG))


@router.callback_query(
    F.data == 'rules_accepted'
)
async def show_main_window(callback: CallbackQuery, user: User):
    try:
        await callback.message.delete_reply_markup()
    except TelegramBadRequest:
        pass
    if user.is_admin:
        keyboard = AdminMainKeyboards.main_window
    else:
        keyboard = MainKeyboards.main_window
    await callback.message.answer(
        text=MainText.main_window,
        reply_markup=keyboard
    )


@router.callback_query(
    F.data == 'show_ads'
)
async def find_or_create_ads(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass
    await callback.message.answer(
        text=MainText.ads_window,
        reply_markup=MainKeyboards.ads_window
    )
    await state.set_state(AdCreationStates.ADS_WINDOW)


@router.callback_query(
    F.data == 'show_profile'
)
async def show_profile(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass
    await callback.message.answer(
        text=MainText.profile_window,
        reply_markup=MainKeyboards.profile_window
    )


@router.callback_query(
    F.data == 'show_user_ads'
)
async def show_user_ads(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass
    await callback.message.answer(
        text=MainText.user_ads_window,
        reply_markup=MainKeyboards.show_user_ads
    )


@router.callback_query(
    F.data == 'show_rules'
)
async def show_rules(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass
    await callback.message.answer(
        text=OnboardingText.rules_one,
        reply_markup=MainKeyboards.show_rules
    )


@router.callback_query(
    F.data == 'show_second_rules'
)
async def show_second_rules(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass
    await callback.message.answer(
        text=OnboardingText.rules_two,
        reply_markup=MainKeyboards.show_second_rules
    )


@router.callback_query(
    F.data == 'create_user_feedback'
)
async def create_user_feedback(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass
    await callback.message.answer(
        text="Напшии обо всем, чем хочешь поделиться с администрацией проекта",
        reply_markup=GeneralKeyboards.to_main_menu
    )
    await state.set_state(FeedbackCreationStates.FEEDBACK_CREATION)


# @router.message()
# async def message_echo(message: Message, state: FSMContext):
#     state = await state.get_state()
#     await message.answer(
#         text=f"Message попал в main_dialog c состоянием {state}"
#     )


# @router.callback_query()
# async def callback_echo(callback: CallbackQuery, state: FSMContext):
#     state = await state.get_state()
#     await callback.message.answer(
#         text=f"Callback попал в main_dialog c состоянием {state}"
#     )
