from asyncio import create_task, sleep

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import ContentType
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.filters.supported_media import SupportedMediaFilter
from app.states.user.user_feedback_creation_states import UserFeedbackCreationStates
from app.states.user.main_states import MainDialogStates
from app.keyboards.user.main_keyboards import MainKeyboards
from app.text.user.main_text import MainDialogText
from app.text.user.user_feedback_creation_text import UserFeedbackCreationText

router = Router()
router.message.filter(StateFilter(UserFeedbackCreationStates.FEEDBACK_CREATION))
router.callback_query.filter(StateFilter(UserFeedbackCreationStates.FEEDBACK_CREATION))


async def _render_main_menu(
    message: Message, state: FSMContext, response: str
):
    try:
        await message.reply(
            text=response,
        )
        await message.answer(
            text=MainDialogText.main_window,
            reply_markup=MainKeyboards.main_window
        )
    except AttributeError:
        await message.message.answer(
            text=response
        )
        await message.message.answer(
            text=MainDialogText.main_window,
            reply_markup=MainKeyboards.main_window
        )
    await state.set_state(MainDialogStates.MAIN_DIALOG)


@router.callback_query(F.data == "to_main_menu")
async def cancel_writing(message: Message, bot: Bot, state: FSMContext):
    await _render_main_menu(
        message, state, UserFeedbackCreationText.unsuccesfull_creation
    )


@router.message(F.text)
async def send_text_message(message: Message, bot: Bot, state: FSMContext):
    if len(message.text) > 4000:
        await message.reply(
            text="Слишком длинное сообщение"
        )
    else:
        await bot.send_message(
            chat_id=-1002080962591,
            text=message.html_text + f"\n\n#id{message.from_user.id}"
        )
    await _render_main_menu(
        message, state, UserFeedbackCreationText.succesfull_creation
    )


@router.message(SupportedMediaFilter())
async def send_supported_media(message: Message, state: FSMContext):
    if message.caption and len(message.caption) > 1000:
        return await message.reply(
            text="Слишком длинное сообщение"
        )
    else:
        await message.copy_to(
            chat_id=-1002080962591,
            caption=((message.caption or "") + f"\n\n#id{message.from_user.id}"),
        )
    await _render_main_menu(
        message, state, UserFeedbackCreationText.succesfull_creation
    )


@router.message()
async def send_unsupported_types(message: Message, state: FSMContext):
    if message.content_type in (
            ContentType.NEW_CHAT_MEMBERS, ContentType.LEFT_CHAT_MEMBER,
            ContentType.VIDEO_CHAT_STARTED, ContentType.VIDEO_CHAT_ENDED,
            ContentType.VIDEO_CHAT_PARTICIPANTS_INVITED,
            ContentType.MESSAGE_AUTO_DELETE_TIMER_CHANGED,
            ContentType.NEW_CHAT_PHOTO, ContentType.DELETE_CHAT_PHOTO,
            ContentType.SUCCESSFUL_PAYMENT,
            ContentType.NEW_CHAT_TITLE, ContentType.PINNED_MESSAGE):
        await message.reply(
            text="Этот тип сообщения не поддерживается"
        )
    await _render_main_menu(
        message, state, UserFeedbackCreationText.succesfull_creation
    )