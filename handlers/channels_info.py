from aiogram.types import Message
from aiogram.types import CallbackQuery

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from aiogram.dispatcher.filters import Text

from db import crud

from bot import dp


@dp.message_handler(text=["Мои каналы"])
async def get_channels(message: Message):
    author = await crud.getAuthor(message.from_user.id)

    channels_keyboard = InlineKeyboardMarkup()

    for channel in author.channels:
        channel_key = InlineKeyboardButton(
            text=f"{channel.title}",
            callback_data=f"get_channel_info:{channel.id}")
        channels_keyboard.add(channel_key)

    await message.reply(text="Ваши каналы: ",
                        reply_markup=channels_keyboard,
                        reply=False)


@dp.callback_query_handler(Text(startswith="get_channel_info"))
async def callbacks_num(call: CallbackQuery):
    print(call.data.split(":")[1])
