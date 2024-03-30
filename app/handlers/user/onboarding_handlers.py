from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.text.user import OnboardingText
from app.keyboards.user import OnboardingKeyboards
from app.states.user import MainStates


router: Router = Router()


@router.message(Command("start"))
async def get_started(message: Message):
    user = message.from_user.username
    if user:
        await message.answer(
            text=OnboardingText.first_message,
            reply_markup=OnboardingKeyboards.rules_check,
        )
    else:
        await message.answer(
            text=OnboardingText.first_message + OnboardingText.no_username,
            reply_markup=OnboardingKeyboards.rules_check,
        )


@router.callback_query(F.data == "init_rules_check")
async def view_first_rules(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text=OnboardingText.rules_one,
        reply_markup=OnboardingKeyboards.accept_first_rules,
    )


@router.callback_query(F.data == "last_rules_check")
async def view_second_rules(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text=OnboardingText.rules_two,
        reply_markup=OnboardingKeyboards.accept_second_rules,
    )
    await state.set_state(MainStates.MAIN_DIALOG)
