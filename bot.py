import asyncio
import logging

from typing import Union

from aiogram import Bot, Dispatcher
from app.handlers.user import main_dialog, onboarding_dialog
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder, Redis
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.types import LinkPreviewOptions
from aiogram.enums.parse_mode import ParseMode

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.config.main_config import load_config, Config
from app.handlers.admin import admin_handlers
from app.middlewares.config import ConfigMiddleware
from app.middlewares.redis import RedisMiddleware
from app.middlewares.database import DBMiddleware
from app.middlewares.data_loader import LoadDataMiddleware
from app.models.database.base import create_pool


def setup_handlers(dp: Dispatcher):
    dp.include_router(onboarding_dialog.router)
    dp.include_router(main_dialog.router)
    dp.include_router(admin_handlers.router)


def setup_middlewares(
    dp: Dispatcher,
    pool: async_sessionmaker[AsyncSession],
    bot_config: Config,
    redis: Redis
) -> None:
    dp.update.outer_middleware(ConfigMiddleware(bot_config))
    dp.update.outer_middleware(DBMiddleware(pool))
    dp.update.outer_middleware(RedisMiddleware(redis))
    dp.update.outer_middleware(LoadDataMiddleware())


def get_storage(config: Config) -> Union[MemoryStorage, RedisStorage]:

    if config.tg_bot.use_redis:
        storage = RedisStorage.from_url(
            url=config.redis.create_uri(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True)
        )
    else:
        storage = MemoryStorage()

    return storage


logger = logging.getLogger(__name__)
log_level = logging.INFO


async def main() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger.info("Bot has started")

    config = load_config('.env')
    storage = get_storage(config=config)
    bot = Bot(
        config.tg_bot.token,
        default=DefaultBotProperties(
            link_preview=LinkPreviewOptions(is_disabled=True),
            parse_mode=ParseMode.HTML,
        )
    )
    dp = Dispatcher(storage=storage)
    setup_handlers(dp)
    setup_middlewares(dp, create_pool(config.db), config, storage.redis)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    finally:
        logger.error("Bot has been stopped")
