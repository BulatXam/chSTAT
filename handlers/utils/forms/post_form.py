from aiogram.dispatcher.filters.state import State, StatesGroup


class PostForm(StatesGroup):
    message = State()
    right_time = State()
