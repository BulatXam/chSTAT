from aiogram.dispatcher.filters.state import State, StatesGroup


class ChannelLinkForm(StatesGroup):
    link = State()
