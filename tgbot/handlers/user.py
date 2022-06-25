import json
from asyncio import sleep
from random import choice

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from aiogram.types import Message, InputFile, ReplyKeyboardRemove, ParseMode

from tgbot.config import load_config
from tgbot.keyboards.inline import CHANEL_LINK
from tgbot.keyboards.reply import MAIN_MENU, EVENTS, ROLE, REVIEW_ANSWER, FAQ, FQ, Events
from tgbot.middlewares.censorship import censor
from tgbot.misc import states, dialogs
from tgbot.middlewares.db import database as db
from tgbot.middlewares.data_cleaner import cleaner
from tgbot.misc.stickers import sticker
from tgbot.services.google_writer import GoogleWriter

conf = load_config('.env')


async def user_start(message: Message, state: FSMContext):
    if await db.insert_user({'tg_id': message.from_user.id, 'username': message.from_user.username}):
        await message.answer(dialogs.Messages.grete_msg, reply_markup=MAIN_MENU)
        await states.data_setter(state, message)
        await states.Graduate.init_user.set()
        return
    await states.Graduate.init_user.set()
    await message.answer(dialogs.Messages.retry_start, reply_markup=MAIN_MENU)


async def get_main_menu(message: Message):
    await message.answer(dialogs.Messages.main_menu_description, reply_markup=MAIN_MENU)
    await states.Graduate.init_user.set()


async def get_event_timing(message: Message):
    await message.answer(dialogs.Messages.event_program, reply_markup=EVENTS)


async def get_programs(message: Message):
    match message.text:
        case Events.main_scene:
            await message.answer_photo(InputFile('data/event_timing/main_scene.jpg'))
        case Events.electroscene:
            await message.answer_photo(InputFile('data/event_timing/electroscene.jpg'))
        case Events.water_show:
            await message.answer_photo(InputFile('data/event_timing/water_show.jpg'))
        case Events.disco_scene:
            await message.answer_photo(InputFile('data/event_timing/disco_scene.jpg'))
        case Events.quiet_disco:
            await message.answer_photo(InputFile("data/event_timing/quiet_disco.png"),
                                       caption=dialogs.NoPicProgram.quiet_disco)
        case Events.game_zone:
            await message.answer_photo(InputFile("data/event_timing/game_zone.png"),
                                       caption=dialogs.NoPicProgram.game_zone)
        case Events.quiz_please:
            await message.answer_photo(InputFile("data/event_timing/quiz_plizz.jpg"),
                                       caption=dialogs.NoPicProgram.quiz_please)
        case Events.comic_show:
            await message.answer_photo(InputFile("data/event_timing/comic_1.jpg"))
            await message.answer_photo(InputFile("data/event_timing/comic_2.jpg"))
            await message.answer_photo(InputFile("data/event_timing/comic_3.jpg"))
        case Events.extreme:
            await message.answer_photo(InputFile("data/event_timing/extreme.png"),
                                       caption=dialogs.NoPicProgram.extreme,
                                 parse_mode=ParseMode.HTML)
        case Events.young_people:
            await message.answer_photo(InputFile("data/event_timing/young_people.png"),
                                       caption=dialogs.NoPicProgram.young_people)


async def get_map(message: Message):
    await message.answer(dialogs.Messages.map)
    await message.answer_photo(photo=InputFile("data/map/map5.jpg"))


async def start_review(message: Message, state: FSMContext):
    repeat_review = await state.get_data()
    if not repeat_review.get('review'):
        if await censor(message.text):
            await states.Review.wait_role.set()
            await message.answer(dialogs.Messages.start_review)
            await sleep(0.5)
            await message.answer(dialogs.Messages.user_role, reply_markup=REVIEW_ANSWER)
            return
        await message.answer(dialogs.Messages.censor_stop)
        return
    await message.answer(dialogs.Messages.retry_review)


async def get_role(message: Message, state: FSMContext):
    if message.text not in conf.commands.cmd:
        match message.text:
            case ROLE.grad:
                # await state.update_data(role=message.text)
                await message.answer(dialogs.Messages.pers_info_for_grad, reply_markup=ReplyKeyboardRemove())
            case ROLE.teacher:
                # await state.update_data(role=message.text)
                await message.answer(dialogs.Messages.pers_info_for_teacher, reply_markup=ReplyKeyboardRemove())
            case ROLE.parents:
                # await state.update_data(role=message.text)
                await message.answer(dialogs.Messages.pers_info_for_parents, reply_markup=ReplyKeyboardRemove())
            case _:
                await message.answer(dialogs.Messages.not_in_answers_list)
                return
        await state.update_data(role=message.text)
        await states.Review.next()
        return
    await message.answer(dialogs.Messages.its_commands)


async def get_pers_info(message: Message, state: FSMContext):
    if message.text not in conf.commands.cmd:
        await state.update_data(pers_info=message.text)
        await message.answer(dialogs.Messages.comment_invite)
        await states.Review.next()
        return
    await message.answer(dialogs.Messages.its_commands)


# Может быть придется собирать отдельно имя и школу
# async def get_school(message: Message, state: FSMContext):
#     if message.text not in conf.commands.cmd:
#         await state.update_data(school=message.text)
#         await message.answer(dialogs.Messages.comment_invite)
#         await states.Review.next()
#         return
#     await message.answer("Это команда")


async def review_done(message: Message, state: FSMContext):
    if await censor(message.text):
        if message.text not in conf.commands.cmd:
            await state.update_data(review=message.text)
            await message.answer(dialogs.Messages.finish_review, reply_markup=MAIN_MENU)
            raw_data = await state.get_data()
            str_state = await state.get_state()
            await db.insert_review(raw_data)
            clear_data = await cleaner(raw_data, str_state)
            review = GoogleWriter(conf.google.review_sheet_id, conf.google.cred_file)
            review.data_writer([clear_data], len(clear_data))
            await states.Graduate.init_user.set()
            return
        await message.answer(dialogs.Messages.its_commands)
        return
    await message.answer(dialogs.Messages.censor_stop)


async def start_msg_to_all(message: Message, state: FSMContext):
    await message.answer(dialogs.Messages.msg_to_all)
    await sleep(0.5)
    await message.answer(dialogs.Messages.name_for_main_chat,
                         reply_markup=ReplyKeyboardRemove())
    await states.Chat.wait_name.set()


async def get_name_for_main_chat(message: Message, state: FSMContext):
    if message.text not in conf.commands.cmd:
        await state.update_data(name=message.text)
        await message.answer(dialogs.Messages.school_for_main_chat)
        await states.Chat.next()
        return
    await message.answer(dialogs.Messages.its_commands)


async def get_school_for_main_chat(message: Message, state: FSMContext):
    try:
        int(message.text)
        if message.text not in conf.commands.cmd:
            await state.update_data(school=message.text)
            await message.answer(dialogs.Messages.text_for_main_chat)
            await states.Chat.next()
            return
        await message.answer(dialogs.Messages.its_commands)
    except ValueError:
        await message.answer("Напиши номер школы цифрами")


async def get_text_for_main_chat(message: Message, state: FSMContext):
    if await censor(message.text.lower()):
        if message.text not in conf.commands.cmd:
            await state.update_data(text=message.text)
            await message.answer(dialogs.Messages.msg_for_main_chat_done,
                                 reply_markup=MAIN_MENU)
            raw_data = await state.get_data()
            str_state = await state.get_state()
            await db.insert_msg_to_all(raw_data)
            clear_data = await cleaner(raw_data, str_state)
            clear_data.append('FALSE')
            chat_msg_writer = GoogleWriter(conf.google.chat_sheet_id, conf.google.cred_file)
            chat_msg_writer.data_writer([clear_data], len(clear_data)+1)
            await states.Graduate.init_user.set()
            return
        await message.answer(dialogs.Messages.its_commands)
        return
    await message.answer(dialogs.Messages.censor_stop)


async def get_photo_link(message: Message):
    await message.answer(dialogs.Messages.tmp_photo_link)


async def sticker_pack(message: Message):
    await message.answer(dialogs.Messages.sticker_pack_first)
    await message.answer_sticker(choice(sticker))


async def online_chat(message: Message):
    await message.answer(dialogs.Messages.online_chat, reply_markup=CHANEL_LINK)


async def get_faq(message: Message):
    await message.answer(dialogs.Messages.faq_description, reply_markup=FAQ)


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
    dp.register_message_handler(get_main_menu, text=[Events.main_menu, FQ.main_menu], state="*")

    dp.register_message_handler(get_event_timing, commands=["event_program"], state="*")
    dp.register_message_handler(get_event_timing, text=MAIN_MENU.values["keyboard"][0][0]['text'], state="*")

    dp.register_message_handler(get_map, commands=["map"], state=states.Graduate.init_user)
    dp.register_message_handler(get_map, text=MAIN_MENU.values["keyboard"][0][1]['text'], state=states.Graduate.init_user)
    dp.register_message_handler(get_programs, text=list(Events.__dict__.values())[2:12], state="*")

    dp.register_message_handler(start_review, commands=["review"], state=states.Graduate.init_user)
    dp.register_message_handler(start_review, text=MAIN_MENU.values["keyboard"][1][0]['text'],
                                state=states.Graduate.init_user)
    dp.register_message_handler(get_role, state=states.Review.wait_role)
    dp.register_message_handler(get_pers_info, state=states.Review.wait_pers_info)
    dp.register_message_handler(review_done, state=states.Review.wait_review)

    dp.register_message_handler(start_msg_to_all, commands=["msg_to_all"], state=states.Graduate.init_user, is_admin=False)
    dp.register_message_handler(start_msg_to_all, text=MAIN_MENU.values["keyboard"][1][1]['text'],
                                state=states.Graduate.init_user, is_admin=False)
    dp.register_message_handler(get_name_for_main_chat, state=states.Chat.wait_name, content_types=ContentType.ANY)
    # dp.register_message_handler(get_grade_for_main_chat, state=states.Chat.wait_grade)
    dp.register_message_handler(get_school_for_main_chat, state=states.Chat.wait_school)
    dp.register_message_handler(get_text_for_main_chat, state=states.Chat.wait_text)

    dp.register_message_handler(get_photo_link, commands=['photo_gallery'],
                                state=states.Graduate.init_user)
    dp.register_message_handler(get_photo_link, text=MAIN_MENU.values["keyboard"][2][0]['text'],
                                state=states.Graduate.init_user)

    dp.register_message_handler(sticker_pack, commands=['stickerpack'], state=states.Graduate.init_user)
    dp.register_message_handler(sticker_pack, text=MAIN_MENU.values["keyboard"][2][1]['text'],
                                state=states.Graduate.init_user)
    # dp.register_message_handler(sticker_catch, state="*")

    dp.register_message_handler(online_chat, commands="msg_to_all", state=states.Graduate.init_user)
    dp.register_message_handler(online_chat, text="Онлайн-чат", state=states.Graduate.init_user)

    dp.register_message_handler(get_faq, commands=['fqa'], state=states.Graduate.init_user)
    dp.register_message_handler(get_faq, text=MAIN_MENU.values["keyboard"][3][1]['text'],
                                state=states.Graduate.init_user)

    dp.register_message_handler(faq_answer, text=[FQ.items, FQ.exit, FQ.timing, FQ.water, FQ.fireworks],
                                state=states.Graduate.init_user)
