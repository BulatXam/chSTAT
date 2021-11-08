from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

add_channel_key = KeyboardButton("Добавить канал")
help_key = KeyboardButton("Помощь")
info_channel_key = KeyboardButton("Мои каналы")

start_keyboard.row(add_channel_key)
start_keyboard.row(help_key, info_channel_key)

