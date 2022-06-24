from asyncio import sleep

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.misc import states


async def bot_echo(message: types.Message):
    text = [
        "Эхо без состояния.",
        "Сообщение:",
        message.text
    ]
    print(message)
    await message.answer('\n'.join(text))


async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    # text = [
    #     f'Эхо в состоянии {hcode(state_name)}',
    #     'Содержание сообщения:',
    #     hcode(message.text)
    # ]
    print()
    try:
        sticker_id = message['sticker']['file_id']
        doc_id = message['document']['file_id']
        if sticker_id:
            await message.answer(sticker_id)
        elif doc_id:
            await message.answer(doc_id)

    except TypeError:
        if state_name == "Review:wait_review":
            text = 'ты хотел оставить отзыв. но видимо передумал. ' \
                   'Если снова решишь написать отзыв, выбери соответсвующую команды '
            await message.answer(text)
            await states.Graduate.init_user.set()
            return



def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
