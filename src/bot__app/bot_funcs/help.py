from aiogram import Bot
from aiogram.types import Message

from src.bot__app.extensions.api_currency import APIConverter
from src.bot__app.extensions.phrases_data import PhrasesData


async def handle_help(bot: Bot, message: Message, api: APIConverter, phrases: PhrasesData):
    await bot.send_message(message.chat.id, phrases.help_text)
