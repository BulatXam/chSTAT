from aiogram.types import CallbackQuery, ContentType, Message

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.utils.forms.post_form import PostForm

from db import crud

from bot import dp

from datetime import datetime

from loguru import logger


@dp.callback_query_handler(Text(startswith="create_post"))
async def create_post(call: CallbackQuery):
    await PostForm.message.set()

    await call.message.reply("Отправьте сообщение, которое вы бы хотели "
                             "выложить(/cancel для отмены):", reply=False)

    logger.info(
        f"User<{call.message.from_user.id}> get PostForm state for create Post"
    )


@dp.message_handler(content_types=ContentType.ANY, state=PostForm.message)
async def get_post_photo(message: Message,
                         state: FSMContext):
    await state.update_data(text=message.text,
                            caption=message.caption)

    files = []
    if message.photo:
        files.append(message.photo[0])

        logger.info(
            f"User<{message.from_user.id}> append "
            f"photo<{message.photo[0].file_id}> to his post")
    if message.audio:
        files.append(message.audio)

        logger.info(
            f"User<{message.from_user.id}> append "
            f"audio<{message.audio.file_id}> to his post")
    if message.document:
        files.append(message.document)

        logger.info(
            f"User<{message.from_user.id}> append "
            f"document<{message.document.file_id}> to his post")

    await state.update_data(files=files)

    await message.reply("Укажите время:")

    await PostForm.next()


@dp.message_handler(state=PostForm.right_time)
async def get_post_right_time(message: Message,
                              state: FSMContext):
    # right_time = datetime(message.text)
    right_time = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    await state.update_data(right_time=right_time)

    logger.info(f"User<{message.from_user.id}> add right_time for his post")

    state_data = await state.get_data()

    await message.reply(state_data, reply=False)

    text = state_data["text"] if state_data["text"] else state_data["caption"]

    post = await crud.createPost(
        text=text,
        files=state_data["files"],
        right_time=state_data["right_time"],
    )

    logger.info(f"User<{message.from_user.id}> add Post<{post.id}> in db")

    await state.finish()
