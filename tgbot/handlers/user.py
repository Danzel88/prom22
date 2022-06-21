import json
from asyncio import sleep

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InputFile, ReplyKeyboardRemove

from tgbot.config import load_config
from tgbot.keyboards.reply import MAIN_MENU, EVENTS, REVIEW_ANSWER, FAQ, FQ
from tgbot.middlewares.censorship import censor
from tgbot.misc import states, dialogs
from tgbot.middlewares.db import database as db
from tgbot.services.google_reader import GoogleDocReader
from tgbot.services.google_writer import GoogleWriter

conf = load_config('.env')


async def user_start(message: Message, state: FSMContext):
    if await db.create_user({'tg_id': message.from_user.id, 'username': message.from_user.username}):
        await message.answer(dialogs.Messages.grete_msg)
        await sleep(0.5)
        await message.answer(dialogs.Messages.grete_msg2, reply_markup=MAIN_MENU)
        await states.Graduate.init_user.set()
        return
    await message.answer(dialogs.Messages.retry_start)


async def get_main_menu(message: Message):
    await message.answer(dialogs.Messages.main_menu, reply_markup=MAIN_MENU)
    await states.Graduate.init_user.set()


async def get_event_timing(message: Message):
    await message.answer(dialogs.Messages.event_program, reply_markup=EVENTS)


async def get_retro_disco(message: Message):
    conf = load_config('.env')
    main_scene_timeline = GoogleDocReader(conf.google.retrodisco, conf.google.cred_file). \
        get_data_from_gdocs()
    await message.answer('\n'.join(main_scene_timeline), parse_mode='HTML')


async def get_map(message: Message):
    await message.answer(dialogs.Messages.map)
    await message.answer_photo(InputFile('data/map/points.png'))


async def start_review(message: Message, state: FSMContext):
    repeat_review = await state.get_data()
    if not repeat_review:
        await states.Review.wait_role.set()
        await message.answer(dialogs.Messages.start_review)
        await sleep(0.5)
        await message.answer(dialogs.Messages.user_role, reply_markup=REVIEW_ANSWER)
        await states.state_setter(state, message)
        return
    await message.answer(dialogs.Messages.retry_review)


async def get_role(message: Message, state: FSMContext):
    if message.text not in conf.commands.cmd:
        for i in REVIEW_ANSWER.values['keyboard']:
            if message.text == i[0]['text']:
                await state.update_data(role=message.text)
                await message.answer(dialogs.Messages.review_name, reply_markup=ReplyKeyboardRemove())
                await states.Review.next()
                return
        await message.answer(dialogs.Messages.not_in_answers_list)
        return
    await message.answer("Это команда")


async def get_name(message: Message, state: FSMContext):
    if message.text not in conf.commands.cmd:
        await state.update_data(name=message.text)
        await message.answer(dialogs.Messages.review_school)
        await states.Review.next()
        return
    await message.answer("Это команда")


async def get_school(message: Message, state: FSMContext):
    if message.text not in conf.commands.cmd:
        await state.update_data(school=message.text)
        await message.answer(dialogs.Messages.comment_invite)
        await states.Review.next()
        return
    await message.answer("Это команда")


async def review_done(message: Message, state: FSMContext):
    if await censor(message.text):
        if message.text not in conf.commands.cmd:
            await state.update_data(review=message.text)
            await message.answer(dialogs.Messages.finish_review, reply_markup=MAIN_MENU)
            data = await state.get_data()
            await db.crete_review(data)
            data = list((await state.get_data()).values())
            del(data[1])
            review = GoogleWriter(conf.google.review_sheet_id, conf.google.cred_file)
            review.data_writer([data], len(data))
            # await state.reset_data()
            await states.Graduate.init_user.set()
            return
        await message.answer('Это команда')
        return
    await message.answer(dialogs.Messages.censor_stop)

async def start_msg_to_all(message: Message, state: FSMContext):
    await states.state_setter(state, message)
    await message.answer(dialogs.Messages.msg_to_all)
    await message.answer(dialogs.Messages.name_for_main_chat,
                         reply_markup=ReplyKeyboardRemove())
    await states.Chat.wait_name.set()


async def get_name_for_main_chat(message: Message, state: FSMContext):
    if message.text not in conf.commands.cmd:
        await state.update_data(name=message.text)
        await message.answer(dialogs.Messages.grade_for_main_chat)
        await states.Chat.next()
        return
    await message.answer('Это команда')


async def get_grade_for_main_chat(message: Message, state: FSMContext):
    if message.text not in conf.commands.cmd:
        await state.update_data(grade=message.text)
        await message.answer(dialogs.Messages.school_for_main_chat)
        await states.Chat.next()
        return
    await message.answer('Это команда')


async def get_school_for_main_chat(message: Message, state: FSMContext):
    if message.text not in conf.commands.cmd:
        await state.update_data(school=message.text)
        await message.answer(dialogs.Messages.text_for_main_chat)
        await states.Chat.next()
        return
    await message.answer('Это команда')


async def get_text_for_main_chat(message: Message, state: FSMContext):
    if await censor(message.text):
        if message.text not in conf.commands.cmd:
            await state.update_data(text=message.text)
            await message.answer(dialogs.Messages.msg_for_main_chat_done,
                                 reply_markup=MAIN_MENU)
            await states.Graduate.init_user.set()
            raw_data = await state.get_data()
            await db.create_msg_to_all(raw_data)
            del(raw_data['username'])
            clear_data = (list(raw_data.values()))
            chat_msg_writer = GoogleWriter(conf.google.chat_sheet_id, conf.google.cred_file)
            chat_msg_writer.data_writer([clear_data], len(clear_data))
            return
        await message.answer('Это команда')
        return
    await message.answer(dialogs.Messages.censor_stop)


async def get_photo_link(message: Message):
    await message.answer(dialogs.Messages.photo_link)


async def sticker_pack(message: Message):
    await message.answer(dialogs.Messages.sticker_pack_first)
    await message.answer_sticker("CAACAgIAAxkBAAIFnmKvKaYh1Jdf5Dc-xbgTZyxq7olcAAJHAQACe04qEC2-TTtxjiCwJAQ")
    await sleep(0.5)
    await message.answer(dialogs.Messages.sticker_pack_second)


async def get_faq(message: Message):
    await message.answer(message.text, reply_markup=FAQ)


async def faq_answer(message: Message):
    questions = []
    for i in FAQ.values["keyboard"]:
        questions.append(i)
    match message.text:
        case FQ.exit:
            await message.answer(dialogs.FaqAnswers.exit_chance)
        case FQ.items:
            await message.answer(dialogs.FaqAnswers.personal_items)
        case FQ.water:
            await message.answer(dialogs.FaqAnswers.water)
        case FQ.timing:
            await message.answer(dialogs.FaqAnswers.timing)
        case FQ.fireworks:
            await message.answer(dialogs.FaqAnswers.fireworks)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")

    dp.register_message_handler(get_main_menu, commands=["menu"], state="*")
    dp.register_message_handler(get_main_menu, text=[EVENTS.values["keyboard"][9][0]['text'], FQ.main_menu], state="*")

    dp.register_message_handler(get_event_timing, commands=["event_program"], state="*")
    dp.register_message_handler(get_event_timing, text=MAIN_MENU.values["keyboard"][0][0]['text'], state="*")

    dp.register_message_handler(get_map, commands=["map"], state=states.Graduate.init_user)
    dp.register_message_handler(get_map, text=MAIN_MENU.values["keyboard"][0][1]['text'], state="*")
    dp.register_message_handler(get_retro_disco, text=EVENTS.values["keyboard"][3][0]['text'], state="*")

    dp.register_message_handler(start_review, commands=["review"], state=states.Graduate.init_user)
    dp.register_message_handler(start_review, text=MAIN_MENU.values["keyboard"][1][0]['text'],
                                state=states.Graduate.init_user)
    dp.register_message_handler(get_role, state=states.Review.wait_role)
    dp.register_message_handler(get_name, state=states.Review.wait_name)
    dp.register_message_handler(get_school, state=states.Review.wait_school)
    dp.register_message_handler(review_done, state=states.Review.wait_review)

    dp.register_message_handler(start_msg_to_all, commands=["msg_to_all"], state=states.Graduate.init_user)
    dp.register_message_handler(start_msg_to_all, text=MAIN_MENU.values["keyboard"][1][1]['text'],
                                state=states.Graduate.init_user)
    dp.register_message_handler(get_name_for_main_chat, state=states.Chat.wait_name)
    dp.register_message_handler(get_grade_for_main_chat, state=states.Chat.wait_grade)
    dp.register_message_handler(get_school_for_main_chat, state=states.Chat.wait_school)
    dp.register_message_handler(get_text_for_main_chat, state=states.Chat.wait_text)

    dp.register_message_handler(get_photo_link, commands=['photo_gallery'],
                                state=states.Graduate.init_user)
    dp.register_message_handler(get_photo_link, text=MAIN_MENU.values["keyboard"][2][0]['text'],
                                state=states.Graduate.init_user)

    dp.register_message_handler(sticker_pack, commands=['stickerpack'], state=states.Graduate.init_user)
    dp.register_message_handler(sticker_pack, text=MAIN_MENU.values["keyboard"][2][1]['text'],
                                state=states.Graduate.init_user)

    dp.register_message_handler(get_faq, commands=['fqa'], state=states.Graduate.init_user)
    dp.register_message_handler(get_faq, text=MAIN_MENU.values["keyboard"][3][1]['text'],
                                state=states.Graduate.init_user)

    dp.register_message_handler(faq_answer, text=[FQ.items, FQ.exit, FQ.timing, FQ.water, FQ.fireworks],
                                state=states.Graduate.init_user)
