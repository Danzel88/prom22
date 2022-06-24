from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

online_chat_btn = InlineKeyboardButton("Онлайн-чат Московского выпускного",
                                       url="https://t.me/prom_2022")

CHANEL_LINK = InlineKeyboardMarkup().add(online_chat_btn)