from aiogram import Bot, Dispatcher
from aiogram import executor

from aiogram.types import Message

from aiogram.utils.exceptions import BadRequest

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from forms import ChannelLinkForm

from keyboards import start_keyboard

import config
import crud

bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands="Hi")
async def cmd_test1(message: Message):
    await message.reply("Hello World")


@dp.message_handler(commands=["start", "help"])
async def start(message: Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text='👋 Привет, с помощью этого бота вы сможете эффективно управлять '
             'своими каналами. Для более подробной информации, '
             'нажмите кнопку "Помощь"',
        reply_markup=start_keyboard
    )


@dp.message_handler(text=["Добавить канал"])
async def add_channel(message: Message):
    await ChannelLinkForm.link.set()

    await bot.send_message(
        chat_id=message.chat.id,
        text="Добавьте нашего бота в ваш телеграм канал с правами админа."
             "Как только добавили-отправьте ссылку на ваш канал сообщением."
    )


@dp.message_handler(state=ChannelLinkForm.link)
async def process_channel_link(message: Message,
                               state: FSMContext):

    channel = await bot.get_chat(chat_id=message.text)

    try:
        admins = await channel.get_administrators()
    except BadRequest:
        # Запрос не произошел, так как бот не вступлен в
        # канал или ему не дали права админа
        await bot.send_message(
            message.chat.id,
            text="Вы не добавили этого бота в канал!"
        )
        return

    try:
        # Получаем создателя чата из всех админов
        channel_owner = \
            [admin for admin in admins if admin.is_chat_creator()][0]
    except IndexError:
        # не существует индекса[0], так как список пуст.
        await bot.send_message(
            message.chat.id,
            text="В этом канале нет создателя!"
        )
        return

    if channel_owner["user"]["id"] == message.from_user.id:
        author = await crud.getOrCreateAuthor(
            id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )

        db_channel = await crud.createChannel(
            id=channel.id,
            author_id=message.from_user.id,
            title=channel.title,
            username=channel.username,
            description=channel.description,
            invite_link=channel.invite_link,
            linked_chat_id=channel.linked_chat_id
        )
        if db_channel:
            author.channels.append(db_channel)

        await bot.send_message(chat_id=message.chat.id,
                               text=f"Канал {channel.title} добавлен!")
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text="Вы не являетесь автором этого канала!")

    # Не добавляем в state никаких записей, так как мы получаем только 1 запись.
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
