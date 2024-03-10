from aiogram import Router
from aiogram.filters import Command, Text, CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.redis import Redis

from app.lexicon.messages import CommandsMessages, UserMessages
from app.config.main_config import Config
from app.dao.holder import HolderDAO
from app.models import dto


router: Router = Router()
router.message.filter(StateFilter(default_state))


@router.message(Command(commands=["start"]))
async def process_help_command(message: Message):
    await message.answer(
        text="Привет!"
    )
