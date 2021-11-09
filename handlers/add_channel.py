from aiogram.types import Message

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from aiogram.utils.exceptions import ChatNotFound, BadRequest

from forms.channel_link_form import ChannelLinkForm

from db import crud

from bot import dp, bot


@dp.message_handler(text=["Добавить канал"])
async def add_channel(message: Message):
    await ChannelLinkForm.link.set()
    await message.reply(
        reply=False,
        text="Добавьте нашего бота в ваш телеграм канал с правами админа."
             "Как только добавили-отправьте ссылку на ваш канал сообщением."
             "(/cancel для отмены)"
    )


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Отмена.')


@dp.message_handler(state=ChannelLinkForm.link)
async def process_channel_link(message: Message,
                               state: FSMContext):
    try:
        channel = await bot.get_chat(chat_id=message.text)
    except ChatNotFound:
        await bot.send_message(chat_id=message.chat.id,
                               text="Чат не найден!")
        return

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
