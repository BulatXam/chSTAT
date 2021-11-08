import config
import aiogram

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from keyboards import start_keyboard

from forms import ChannelLinkForm

from aiogram.dispatcher import FSMContext

import crud

bot = aiogram.Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)


@dp.message_handler(commands="Hi")
async def cmd_test1(message: aiogram.types.Message):
    await message.reply("Hello World")


@dp.message_handler(commands=["start", "help"])
async def start(message: aiogram.types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text='👋 Привет, с помощью этого бота вы сможете эффективно управлять '
             'своими каналами. Для более подробной информации, '
             'нажмите кнопку "Помощь"',
        reply_markup=start_keyboard
    )


@dp.message_handler(text=["Добавить канал"])
async def add_channel(message: aiogram.types.Message):
    await ChannelLinkForm.link.set()

    await bot.send_message(
        chat_id=message.chat.id,
        text="Добавьте нашего бота в ваш телеграм канал с правами админа."
             "Как только добавили-отправьте ссылку на ваш канал сообщением."
    )


@dp.message_handler(state=ChannelLinkForm.link)
async def process_channel_link(message: aiogram.types.Message,
                               state: FSMContext):

    channel = await bot.get_chat(chat_id=message.text)

    admins = await channel.get_administrators()

    # Получаем создателя чата из всех админов
    channel_owner = \
        [admin for admin in admins if admin.is_chat_creator()][0]

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
        author.channels.append(db_channel)

        await bot.send_message(chat_id=message.chat.id,
                               text=f"Канал {channel.title} добавлен!")
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text="Вы не являетесь автором этого канала!")

    # Не добавляем в state никаких записей, так как мы получаем только 1 запись.
    await state.finish()


if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)
