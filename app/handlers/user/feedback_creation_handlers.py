from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import ContentType
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.states.user import FeedbackCreationStates, MainStates
from app.filters.supported_media import SupportedMediaFilter
from app.keyboards.user import MainKeyboards
from app.text.user import MainText, FeedbackCreationText
from app.services.user import render_response_text


router = Router()

router.message.filter(
    StateFilter(FeedbackCreationStates.FEEDBACK_CREATION)
)
router.callback_query.filter(
    StateFilter(FeedbackCreationStates.FEEDBACK_CREATION)
)


async def _render_main_menu(
    message: Message, state: FSMContext, response: str
):
    try:
        await message.reply(
            text=response,
        )
        await message.answer(
            text=MainText.main_window,
            reply_markup=MainKeyboards.main_window
        )
    except AttributeError:
        await message.message.answer(
            text=response
        )
        await message.message.answer(
            text=MainText.main_window,
            reply_markup=MainKeyboards.main_window
        )
    await state.set_state(MainStates.MAIN_DIALOG)


@router.callback_query(F.data == "to_main_menu")
async def cancel_writing(message: Message, bot: Bot, state: FSMContext):
    await _render_main_menu(
        message, state, FeedbackCreationText.unsuccesfull_creation
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
            text=render_response_text(message)
        )
    await _render_main_menu(
        message, state, FeedbackCreationText.succesfull_creation
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
            caption=render_response_text(message, is_media=True),
        )
    await _render_main_menu(
        message, state, FeedbackCreationText.succesfull_creation
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
        message, state, FeedbackCreationText.succesfull_creation
    )
