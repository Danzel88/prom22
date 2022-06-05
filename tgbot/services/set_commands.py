from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_command(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('event_timing', 'Расписание мероприятия'),
            BotCommand('map', 'Карта'),
            BotCommand('lineup', 'Лайнап'),
            BotCommand('review', 'Отправить отзыв'),
            BotCommand('msg_to_all', 'Сообщение на общие экраны'),
            BotCommand('stickerpack', 'Фраза для стикерпака'),
            BotCommand('photo_gallery', 'Фотоальбом'),
            BotCommand('faq', 'Справка'),
        ]
    )