import warnings

from aiogram import types, Bot
from aiogram.dispatcher.filters import IDFilter
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import asyncio
import datetime
import json
import logging
from aiogram.utils.exceptions import MessageToDeleteNotFound
from tgbot.misc import states
from tgbot.misc.states import Sender, PostToChannel
# from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
# from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import exceptions
from tgbot.misc.dialogs import SenderMessages
from tgbot.config import load_config
from tgbot.middlewares.db import database as db
from tgbot.services.google_reader import GoogleSheetReader


config = load_config('.env')

bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


async def admin_start(message: Message):
    await message.reply("Hello, admin!")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)


# formatter = '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)'
# logging.basicConfig(
#     filename=f'tgbot/log/log-from-sender{datetime.datetime.now().date()}.log',
#     filemode='w',
#     format=formatter,
#     datefmt='%Y-%m-%d %H:%M:%S',
#     level=logging.WARNING
# )
#
# logger = logging.getLogger(__name__)





async def init_sender_state(message: types.Message):
    """инициализация рассылки"""
    if "test" in message.text:
        await message.answer(f'{SenderMessages.message_for_test_sender}', parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
        await Sender.waiting_message_from_admin_to_test_mailing.set()
        return
    await message.answer(f'{SenderMessages.message_for_sender}', parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
    await Sender.waiting_message_from_admin.set()


async def send_message(message: types.Message,
                       user_id: int, disable_notification: bool = False) -> bool:
    """Отправка сообщений"""
    try:
        if message.text is not None:
            await bot.get_session()
            await bot.send_message(chat_id=user_id, text=message.text,
                                   disable_notification=disable_notification,
                                   parse_mode="HTML")
        elif message.photo is not None:
            await bot.get_session()
            await bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id, caption=message.caption,
                                 disable_notification=disable_notification, parse_mode="HTML")
    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logging.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id=user_id, message=message)
    except exceptions.UserDeactivated:
        logging.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logging.warning(f"Target [ID:{user_id}]: failed")
    else:
        logging.warning(f"Target [ID:{user_id}]: success.")
        return True
    await bot.session.close()
    return False


async def test_sender(message: types.Message, state: FSMContext):
    """тестовая рассылка. Сообщение придет только админу"""
    sent_message = {}
    # for u in config.tg_bot.admin_ids:
    try:
        await send_message(user_id=message.from_user.id, message=message)
        sent_message[message.from_user.id] = message.message_id + 1
        await bot.session.close()
    except IndexError:
        logging.error(f'нет пользователей для отправки')
    finally:
    #     with open(f"sender_data/{message.message_id + 1}.json", 'w') as f:
    #         json.dump(sent_message, f)
        await message.answer(f'Номер рассылки для удаления {int(message.message_id) + 1}')
        await state.finish()



async def start_spam(message: types.Message, state: FSMContext):
    """Запуск рассылки. Получаем всех пользователей из БД. Шарашим по айдишникам из спика и в дикт пишем пару
    tg_id: message_id, (дампим в json с именем message_id первого отпавленного сообщения, админ получит
    ответом этот номер) что бы иметь возможность удалить потом рассылку (для этого нужно указывать id чата,
    он же tg_id и message_id) message_id инкерентируюем +1 с каждым следующим отправленным сообщением"""
    logging.warning(f'Запущена рассылка')
    all_users = await db.get_all_users()
    users_list = tuple(zip(*all_users))
    count = 0
    sent_message = {}
    try:
        for user_id in users_list[0]:
            if await send_message(user_id=user_id, message=message):
                sent_message[user_id] = message.message_id + 1 + count
                count += 1
            await asyncio.sleep(.05)
    except IndexError:
        logging.error(f'нет пользователей для отправки')
    finally:
        await message.answer(f'Номер рассылки для удаления {int(message.message_id) + 1}')
        await state.finish()
        logging.warning(f'{count} сообщений отправлено')
        with open(f"sender_data/{message.message_id + 1}.json", 'w') as f:
            json.dump(sent_message, f)


async def del_init(message: types.Message):
    """инициализация удаления рассылки"""
    await message.answer(f'Пришли номер рассылки которую нужно удалить')
    await Sender.waiting_message_id.set()
    logging.warning(f'Пользователем {message.from_user.id} запущено удаление рассылки')


async def delete_send_message(message: types.Message, state: FSMContext):
    """Метод получем номер рассылки, по этому имени получет json файл и из каждого чата удаяет сообщение с
    соответсвующим id. Как формируется это файл описано в start_spam"""
    try:
        await bot.get_session()
        with open(f'sender_data/{message.text}.json') as f:
            data = json.load(f)
        for k in data:
            await bot.delete_message(chat_id=k, message_id=data[k])
        await asyncio.sleep(0.5)
        await state.finish()
        await message.answer(f"Расcылка {message.text} удалена у всех получателей")
        logging.warning(f'Рассылка {message.text} удалена')
    except (FileNotFoundError, MessageToDeleteNotFound):
        logging.warning(f'Mailing number {message.text} not found')
        await message.answer("Нет рассылки с таким номером")
        await bot.session.close()
    await bot.session.close()


async def posts_init(message: Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True).row('Yes').row('No')
    await message.answer("Могу собрать сообщения и отправить в канал? Вы все их проверили?", reply_markup=kb)
    await PostToChannel.wait_confirm_posting.set()


async def post_to_channel(message: Message):
    raw_data = GoogleSheetReader(config.google.chat_sheet_id, config.google.cred_file)
    data = raw_data.get_data_from_gsheet()
    await PostToChannel.first()
    await bot.get_session()
    await bot.send_message(chat_id='-1001643778907', text=data[0])
    await bot.session.close()
    await message.answer("Сообщения ушли", reply_markup=ReplyKeyboardRemove())


def register_sender(dp: Dispatcher):
    dp.register_message_handler(init_sender_state,  commands=["sender", "test"], state="*", is_admin=True)
    # dp.register_message_handler(init_sender_state, commands="test", state="*", is_admin=True)
    dp.register_message_handler(del_init, commands="delete", state="*", is_admin=True)
    dp.register_message_handler(delete_send_message, state=Sender.waiting_message_id, is_admin=True)
    dp.register_message_handler(start_spam, state=Sender.waiting_message_from_admin,
                                content_types=['text', 'photo'], is_admin=True)
    dp.register_message_handler(test_sender, state=Sender.waiting_message_from_admin_to_test_mailing,
                                content_types=['text', 'photo'], is_admin=True)
    dp.register_message_handler(posts_init, commands='post', state="*", is_admin=True)
    dp.register_message_handler(post_to_channel, state=PostToChannel.wait_confirm_posting, is_admin=True)