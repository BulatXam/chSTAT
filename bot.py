from aiogram import Bot, Dispatcher
from aiogram.utils.executor import start_polling

from aiogram import types

from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

if __name__ == "__main__":
    # Импортируем все хендлеры пакета, чтобы диспетчер их увидел
    from handlers import *
    start_polling(dp, skip_updates=True)
