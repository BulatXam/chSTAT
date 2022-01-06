from aiogram.dispatcher.filters.state import State, StatesGroup


class ChannelLinkForm(StatesGroup):
    link = State()


class PostForm(StatesGroup):
    message = State()
    right_time = State()
