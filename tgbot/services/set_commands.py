from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.types.bot_command_scope import BotCommandScopeAllChatAdministrators


async def set_default_command(bot: Bot):
    await bot.get_session()
    return await bot.set_my_commands(
        commands=[
            BotCommand('menu', 'Главное меню'),
            BotCommand('event_program', 'Программа'),
            BotCommand('map', 'Карта'),
            BotCommand('review', 'Отзывы'),
            BotCommand('msg_to_all', 'Сообщение в чат или на экран'),
            BotCommand('photo_gallery', 'Фотоальбом'),
            BotCommand('stickerpack', 'Стикерпак'),
            BotCommand('chat_on', 'Онлайн-чат'),
            BotCommand('faq', 'Справка'),
        ]
    )


async def set_admin_command(bot: Bot):
    await bot.get_session()
    return await bot.set_my_commands(
        commands=[BotCommand('sender', 'Запуск рассылки'),
                  BotCommand('test', 'Запуск тестовой рассылки'),
                  BotCommand('delete', 'Удаление рассылки'),
                  BotCommand('post', 'Запустить отправку сообщений в канал')
                  ],
        scope=BotCommandScopeAllChatAdministrators()
    )
