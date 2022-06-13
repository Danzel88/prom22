import json
from asyncio import sleep

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile, ReplyKeyboardRemove

from tgbot.keyboards.reply import MAIN_MENU, EVENTS, REVIEW_ANSWER
from tgbot.middlewares.censorship import censor
from tgbot.misc import states, dialogs
from tgbot.middlewares.db import database as db


async def user_start(message: Message, state: FSMContext):
    st = await states.state_setter(state, message)
    if db.create_user(st):
        await message.answer(dialogs.Messages.grete_msg)
        await sleep(0.5)
        await message.answer(dialogs.Messages.grete_msg2, reply_markup=MAIN_MENU)
        await states.Graduate.init_user.set()
        return
    await message.answer(dialogs.Messages.retry_start)


async def get_main_menu(message: Message):
    await message.answer(dialogs.Messages.main_menu, reply_markup=MAIN_MENU)


async def get_event_timing(message: Message):
    await message.answer(dialogs.Messages.event_program, reply_markup=EVENTS)


async def get_map(message: Message):
    await message.answer(dialogs.Messages.map)
    await message.answer_photo(InputFile('data/map/points.png'))


async def start_review(message: Message, state: FSMContext):
    await states.Review.wait_role.set()
    await message.answer(dialogs.Messages.start_review)
    await sleep(0.5)
    await message.answer(dialogs.Messages.user_role, reply_markup=REVIEW_ANSWER)
    await states.state_setter(state, message)


async def get_role(message: Message, state: FSMContext):
    for i in REVIEW_ANSWER.values['keyboard']:
        if message.text == i[0]['text']:
            await state.update_data(role=message.text)
            await message.answer(dialogs.Messages.personal_info, reply_markup=ReplyKeyboardRemove())
            await states.Review.next()
            return
    await message.answer(dialogs.Messages.not_in_answers_list)


async def get_personal_info(message: Message, state: FSMContext):
    await state.update_data(pers_info=message.text)
    await message.answer(dialogs.Messages.comment_invite)
    await states.Review.next()


async def review_done(message: Message, state: FSMContext):
    await state.update_data(review=message.text)
    await message.answer(dialogs.Messages.review_done, reply_markup=MAIN_MENU)
    data = await state.get_data()
    db.crete_review(data)
    await states.Graduate.init_user.set()


async def start_msg_to_all(message: Message, state: FSMContext):
    await states.state_setter(state, message)
    await message.answer(dialogs.Messages.msg_to_all)
    await message.answer(dialogs.Messages.name_for_main_chat,
                         reply_markup=ReplyKeyboardRemove())
    await states.Chat.wait_name.set()


async def get_name_for_main_chat(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(dialogs.Messages.grade_for_main_chat)
    await states.Chat.next()


async def get_grade_for_main_chat(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    await message.answer(dialogs.Messages.school_for_main_chat)
    await states.Chat.next()


async def get_school_for_main_chat(message: Message, state: FSMContext):
    await state.update_data(school=message.text)
    await message.answer(dialogs.Messages.text_for_main_chat)
    await states.Chat.next()


async def get_text_for_main_chat(message: Message, state: FSMContext):
    if await censor(message.text):
        await state.update_data(text=message.text)
        await message.answer(dialogs.Messages.msg_for_main_chat_done)
        await states.Graduate.init_user.set()
        data = await state.get_data()
        db.create_msg_to_all(data)
        return
    await message.answer(dialogs.Messages.censor_stop)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")

    dp.register_message_handler(get_main_menu, commands=["menu"], state="*")
    dp.register_message_handler(get_main_menu, text=EVENTS.values["keyboard"][9][0]['text'], state="*")

    dp.register_message_handler(get_event_timing, commands=["event_program"], state="*")
    dp.register_message_handler(get_event_timing, text=MAIN_MENU.values["keyboard"][0][0]['text'], state="*")

    dp.register_message_handler(get_map, commands=["map"], state=states.Graduate.init_user)
    dp.register_message_handler(get_map, text=MAIN_MENU.values["keyboard"][0][1]['text'], state="*")

    dp.register_message_handler(start_review, commands=["review"], state=states.Graduate.init_user)
    dp.register_message_handler(start_review, text=MAIN_MENU.values["keyboard"][1][0]['text'], state=states.Graduate.init_user)
    dp.register_message_handler(get_role, state=states.Review.wait_role)
    dp.register_message_handler(get_personal_info, state=states.Review.wait_personal_info)
    dp.register_message_handler(review_done, state=states.Review.wait_review)

    dp.register_message_handler(start_msg_to_all, commands=["msg_to_all"], state=states.Graduate.init_user)
    dp.register_message_handler(start_msg_to_all, text=MAIN_MENU.values["keyboard"][1][1]['text'], state=states.Graduate.init_user)
    dp.register_message_handler(get_name_for_main_chat, state=states.Chat.wait_name)
    dp.register_message_handler(get_grade_for_main_chat, state=states.Chat.wait_grade)
    dp.register_message_handler(get_school_for_main_chat, state=states.Chat.wait_school)
    dp.register_message_handler(get_text_for_main_chat, state=states.Chat.wait_text)
