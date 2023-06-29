from aiogram import Bot
from aiogram.types import Message

from src.bot__app.app import lang
from src.bot__app.extensions.api_currency import API
from src.bot__db.app import db_flask_app
from src.bot__db.models.helpers import translation_db_repo


async def handle_help(bot: Bot, message: Message, api: API):
    text = translation_db_repo.get_by_lang_phrase(lang, 'help')
    await bot.send_message(message.chat.id, text)
