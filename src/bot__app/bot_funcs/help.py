from aiogram import Bot
from aiogram.types import Message

from src.bot__app.app import bot_app
from src.bot__app.extensions.api_currency import API
from src.bot__app.model_response.translation import ApiTranslationResponse
from src.configs.bot_app__config import LANG_SETTING
from src.configs.internal_api import internal_api


async def handle_help(bot: Bot, message: Message, api: API):
    with bot_app.app.app_context():
        text = internal_api.request_get(f'/translations/{LANG_SETTING}/help', payload_type=ApiTranslationResponse)
    await bot.send_message(message.chat.id, text.translation_content)
