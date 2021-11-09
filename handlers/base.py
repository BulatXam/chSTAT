from aiogram.types import Message

from .keyboards import start_keyboard

from bot import dp


@dp.message_handler(commands="Hi")
async def cmd_test1(message: Message):
    await message.reply("Hello World")


@dp.message_handler(commands=["start", "help"])
async def start(message: Message):
    print("hello")
    await message.reply(
        reply=False,
        text='👋 Привет, с помощью этого бота вы сможете эффективно управлять '
             'своими каналами. Для более подробной информации, '
             'нажмите кнопку "Помощь"',
        reply_markup=start_keyboard
    )