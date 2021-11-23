from aiogram.types import Message

from handlers.utils.keyboards import start_keyboard

from bot import dp

from loguru import logger


@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.reply(
        reply=False,
        text='👋 Привет, с помощью этого бота вы сможете эффективно управлять '
             'своими каналами. Для более подробной информации, '
             'нажмите кнопку "Помощь"',
        reply_markup=start_keyboard
    )
    logger.info(
        f"User<{message.from_user.id}> start to use bot"
    )


@dp.message_handler(text=["Помощь", "/help"])
async def help_cmd(message: Message):
    await message.reply(
        reply=False,
        text='👋 Привет, с помощью этого бота вы сможете эффективно управлять '
             'своими каналами. Для более подробной информации, '
             'нажмите кнопку "Помощь"',
        reply_markup=start_keyboard
    )

    logger.info(f"User<{message.from_user.id}> asked for help-command")
