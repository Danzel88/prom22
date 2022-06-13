from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_command(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('menu', 'Главное меню'),
            BotCommand('event_program', 'Программа'),
            BotCommand('map', 'Карта'),
            BotCommand('review', 'Отзывы'),
            BotCommand('msg_to_all', 'Сообщение на экран'),
            BotCommand('photo_gallery', 'Фотоальбом'),
            BotCommand('stickerpack', 'Стикерпак'),
            BotCommand('faq', 'Справка'),
        ]
    )
