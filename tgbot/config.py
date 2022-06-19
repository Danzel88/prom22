from dataclasses import dataclass

import typing
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from environs import Env


@dataclass
class DbConfig:
    host: str
    # password: str
    # user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool



@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Commands:
    cmd: list[str]


@dataclass
class Google:
    cred_file: str
    chat_sheet_id: str
    review_sheet_id: str
    stickerpack_sheet_id: str
    retrodisco: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous
    commands: Commands
    google: Google


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            # password=env.str('DB_PASS'),
            # user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
        ),
        misc=Miscellaneous(),
        commands=Commands(
            cmd=list(map(str, env.list("COMMANDS")))
        ),
        google=Google(
            cred_file=env.str("CREDFILE"),
            chat_sheet_id=env.str("PROM_CHAT_SHEET_ID"),
            review_sheet_id=env.str("PROM_REVIEW_SHEET_ID"),
            stickerpack_sheet_id=env.str("STICKERPACK_SHEET_ID"),
            retrodisco=env.str("RETRODISCO_ID")
        )

    )


@dataclass
class ListOfButtons:
    text: typing.List
    callback: typing.List = None
    align: typing.List[int] = None

    @property
    def inline_keyboard(self):
        return generate_inline_keyboard(self)

    @property
    def reply_keyboard(self):
        return generate_reply_keyboard(self)


def generate_inline_keyboard(args: ListOfButtons) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    if args.text and args.callback and not (len(args.text) == len(args.callback)):
        raise IndexError("Все списки должны быть одной длины!")

    if not args.align:
        for num, button in enumerate(args.text):
            keyboard.add(InlineKeyboardButton(text=str(button),
                                              callback_data=str(args.callback[num])))
    else:
        count = 0
        for row_size in args.align:
            keyboard.row(*[InlineKeyboardButton(text=str(text), callback_data=str(callback_data))
                           for text, callback_data in
                           tuple(zip(args.text, args.callback))[count:count + row_size]])
            count += row_size
    return keyboard


def generate_reply_keyboard(args: ListOfButtons) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    if not args.align:
        for num, button in enumerate(args.text):
            keyboard.add(KeyboardButton(text=str(button)))
    else:
        count = 0
        for row_size in args.align:
            keyboard.row(*[KeyboardButton(text=str(text)) for text in args.text[count:count + row_size]])
            count += row_size
    return keyboard
