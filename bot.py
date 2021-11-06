import config
import aiogram

bot = aiogram.Bot(token=config.TOKEN)
dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands="Hi")
async def cmd_test1(message: aiogram.types.Message):
    await message.reply("Hello World")


if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=True)
