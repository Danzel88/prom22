import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Config


class CommandFilter(BoundFilter):
    key = 'is_command'

    def __init__(self, is_command: typing.Optional[bool] = None):
        self.is_command = is_command

    async def check(self, obj):
        if self.is_command is None:
            return False
        config: Config = obj.bot.get('config')
        return (obj.text in config.commands.cmd) == self.is_command
