from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.types.bot_command_scope import BotCommandScopeAllChatAdministrators


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


async def set_admin_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[BotCommand('test_sender', 'Запуск тестовой рассылки'),
                  BotCommand('sender', 'Запуск рассылки'),
                  BotCommand('del_sender', 'Удаление рассылки')
        ],
        scope=BotCommandScopeAllChatAdministrators()
        )
