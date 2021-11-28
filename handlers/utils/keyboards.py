from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from db.models import Channel

from aiogram.utils.callback_data import CallbackData

# Callbacks

get_channel = CallbackData("get_channel", "channel_id")
get_my_channels = CallbackData("get_my_channels", "author_id")

create_post = CallbackData("create_post", "channel_id")
get_channel_posts = CallbackData("get_channels_posts", "channel_id")

################################################################################


start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

add_channel_key = KeyboardButton("Добавить канал")
help_key = KeyboardButton("Помощь")
info_channel_key = KeyboardButton("Мои каналы")

start_keyboard.row(add_channel_key)
start_keyboard.row(help_key, info_channel_key)


################################################################################
#                            Добавить канал
#            Помощь                                 Мои каналы
################################################################################


def get_channel_func_keyboard(channel: Channel):
    channel_functions_keyboard = InlineKeyboardMarkup()

    channel_stats_key = InlineKeyboardButton(
        "Статистика канала",
        callback_data=get_channel.new(channel_id=channel.id))
    create_post_key = InlineKeyboardButton(
        "Добавить пост",
        callback_data=create_post.new(channel_id=channel.id)
    )
    my_post_key = InlineKeyboardButton(
        "Мои посты",
        callback_data=get_channel_posts.new(channel_id=channel.id)
    )

    channel_functions_keyboard.row(channel_stats_key)
    channel_functions_keyboard.row(create_post_key, my_post_key)

    return channel_functions_keyboard


################################################################################
#                     Статистика канала {title}
#          Добавить пост                       Мои посты
################################################################################


def get_channels_keyboard(channels: list[Channel]):
    channels_keyboard = InlineKeyboardMarkup()

    for channel in channels:
        channel_key = InlineKeyboardButton(
            text=f"{channel.title}",
            callback_data=get_channel.new(channel_id=channel.id),
        )
        channels_keyboard.add(channel_key)

    return channels_keyboard


################################################################################
#                             Мой канал 1
#                             Мой канал 2
################################################################################
