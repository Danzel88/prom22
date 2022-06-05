from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Graduate(StatesGroup):
    init_user = State()


class Review(StatesGroup):
    wait_review = State()
    review_done = State()


class Chat(StatesGroup):
    wait_review = State()


async def state_setter(state: FSMContext, message):
    await state.update_data(tg_id=message.from_user.id,
                            username=message.from_user.username)
    user_state = await state.get_data()
    return user_state
