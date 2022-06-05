import json

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile
from data.event_timing.timing import EVENT

from tgbot.misc import states, dialogs
from tgbot.middlewares.db import database as db


async def user_start(message: Message, state: FSMContext):
    st = await states.state_setter(state, message)
    if db.create_user(st):
        await message.answer(dialogs.Messages.grete_msg)
        await states.Graduate.init_user.set()
        return
    await message.answer(dialogs.Messages.retry_start)


async def get_event_timing(message: Message):
    event = json.dumps(EVENT)
    await message.answer(event)


async def get_map(message: Message):
    await message.answer_photo(InputFile('data/map/points.png'))


async def get_lineup(message: Message):
    await message.answer_photo(InputFile('data/lineup/lineUp.jpg'))


async def start_review(message: Message, state: FSMContext):
    await states.Review.wait_review.set()
    await message.answer(dialogs.Messages.start_review)
    await states.state_setter(state, message)


async def get_review(message: Message, state: FSMContext):
    await state.update_data(review=message.text)
    rev = await state.get_data()
    db.crete_review(rev)
    await states.Review.next()
    await message.answer(dialogs.Messages.finish_review)


async def start_msg_to_all(message: Message, state: FSMContext):
    await states.Chat.wait_review.set()
    await message.answer(dialogs.Messages.start_common_chat)
    await states.state_setter(state, message)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(get_event_timing, commands=["event_timing"],
                                state=states.Graduate.init_user)
    dp.register_message_handler(get_map, commands=["map"], state=states.Graduate.init_user)
    dp.register_message_handler(get_lineup, commands=["lineup"], state=states.Graduate.init_user)
    dp.register_message_handler(start_review, commands=["review"],
                                state=states.Graduate.init_user)
    dp.register_message_handler(get_review, state=states.Review.wait_review, is_command=False)
    dp.register_message_handler(start_msg_to_all, state=states.Graduate.init_user)
