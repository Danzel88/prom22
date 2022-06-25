from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Graduate(StatesGroup):
    init_user = State()


class Review(StatesGroup):
    wait_role = State()
    wait_pers_info = State()
    wait_review = State()


class Chat(StatesGroup):
    wait_name = State()
    # wait_grade = State()
    wait_school = State()
    wait_text = State()


class Sender(StatesGroup):
    waiting_init_admin = State()
    waiting_message_from_admin = State()
    waiting_message_from_admin_to_test_mailing = State()
    waiting_message_id = State()


class PostToChannel(StatesGroup):
    wait_confirm_posting = State()


async def data_setter(state: FSMContext, message):
    if message.from_user.username:
        await state.update_data(tg_id=message.from_user.id,
                                username=message.from_user.username)
    else:
        await state.update_data(tg_id=message.from_user.id,
                                username='noname')
    user_state = await state.get_data()
    return user_state
