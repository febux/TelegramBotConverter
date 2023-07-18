from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from src.bot__app.extensions.api_currency import APIConverter
from src.bot__app.extensions.phrases_data import PhrasesData


async def handle_start(bot: Bot, message: Message, api: APIConverter, phrases: PhrasesData):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        KeyboardButton(phrases.keyboard_button_1),
        KeyboardButton(phrases.keyboard_button_2),
        KeyboardButton(phrases.keyboard_button_3),
        KeyboardButton(phrases.keyboard_button_4),
    )

    await bot.send_message(message.chat.id, f"{phrases.welcome}, {message.from_user.first_name}!")
    await bot.send_message(message.chat.id, phrases.start, reply_markup=markup)
