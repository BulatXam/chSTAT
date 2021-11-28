from aiogram.types import CallbackQuery

from handlers.utils.keyboards import get_channels_keyboard, \
    get_channel_func_keyboard

from aiogram.types import Message

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from aiogram.utils.exceptions import ChatNotFound, BadRequest

from handlers.utils.forms.channel_link_form import ChannelLinkForm
from handlers.utils.keyboards import get_channel

from db import crud

from bot import dp, bot

from loguru import logger


@dp.message_handler(text=["Мои каналы"])
async def get_channels(message: Message):
    author = await crud.getOrCreateAuthor(message.from_user.id,
                                          message.from_user.first_name,
                                          message.from_user.last_name,
                                          message.from_user.username)
    if author.channels:
        channels_keyboard = get_channels_keyboard(author.channels)

        await message.reply(text="Ваши каналы: ",
                            reply_markup=channels_keyboard,
                            reply=False)

    logger.info(f"User<{message.from_user.id}> get his channels")


@dp.callback_query_handler(get_channel.filter())
async def get_channel(call: CallbackQuery, callback_data: dict[str, str]):
    channel_id = callback_data["channel_id"]

    channel = await crud.getChannel(id=channel_id)

    await call.answer(text=f"Канал {channel.title}")

    channel_functions_keyboard = get_channel_func_keyboard(channel)

    await call.message.reply(text=f"{channel.get_info()}", reply=False,
                             reply_markup=channel_functions_keyboard)

    logger.info(
        f"User<{call.message.from_user.id}> get Channel<{channel.id}> info"
    )


@dp.message_handler(text=["Добавить канал"])
async def add_channel(message: Message):
    await ChannelLinkForm.link.set()
    await message.reply(
        reply=False,
        text="Добавьте нашего бота в ваш телеграм канал с правами админа."
             "Как только добавили-отправьте ссылку на ваш канал сообщением."
             "(/cancel для отмены)"
    )

    logger.info(f"User<{message.from_user.id}> get ChannelLinkForm state for "
                f"add channel")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Отмена.')

    logger.info(f"User<{message.from_user.id}> cancel state")


@dp.message_handler(state=ChannelLinkForm.link)
async def process_channel_link(message: Message,
                               state: FSMContext):
    try:
        channel = await bot.get_chat(chat_id=message.text)
    except ChatNotFound:
        await bot.send_message(chat_id=message.chat.id,
                               text="Чат не найден!")
        logger.error(
            f"User<{message.from_user.id}> tried to add a channel that does "
            f"not have a bot!")
        return

    try:
        admins = await channel.get_administrators()
    except BadRequest:
        await bot.send_message(
            message.chat.id,
            text="Вы не добавили этого бота в канал!"
        )
        logger.error(
            f"User<{message.from_user.id}> is not owner this channel!"
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
        logger.error(
            f"User<{message.from_user.id}> add channel in which no creator"
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
        logger.info(
            f"User<{message.from_user.id}> add Channel<{channel.id}> in db"
        )
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text="Вы не являетесь автором этого канала!")
        logger.error(
            f"User<{message.from_user.id}> try add Channel<{channel.id}> in db,"
            f" but he not creator this channel"
        )

    # Не добавляем в state никаких записей, так как мы получаем только 1 запись.
    await state.finish()
