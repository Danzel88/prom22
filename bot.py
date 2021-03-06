import asyncio
import datetime
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.filters.command import CommandFilter
from tgbot.handlers.admin import register_admin, register_sender
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.services.set_commands import set_default_command, set_admin_command
from tgbot.middlewares.db import database as db

logger = logging.getLogger(__name__)

config = load_config(".env")

def register_all_middlewares(dp):
    pass
    # dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(CommandFilter)


def register_all_handlers(dp):
    # register_admin(dp)
    register_user(dp)
    register_sender(dp)
    # register_echo(dp)


async def set_all_command(bot: Bot):
    await set_default_command(bot)
    await set_admin_command(bot)


async def main():
    logging.basicConfig(
        filename=f'tgbot/log/log-from-bot{datetime.datetime.now().date()}.log',
        filemode='w',
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    storage = RedisStorage2('localhost',
                            6379,
                            db=4,
                            pool_size=10,
                            prefix='Graduates22') if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)
    await set_all_command(bot)
    try:
        # await bot.get_session()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        db._conn.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
