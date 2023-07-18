import os

from aiogram import Bot, Dispatcher

from extensions.api_currency import APIConverter
from src.bot__app.extensions.phrases_data import PhrasesData
from src.utils.app_utils.initial import FlaskApp

tg_token = os.environ['TG_TOKEN']
lang = os.environ['LANG_SETTING']

bot = Bot(token=tg_token)
dp = Dispatcher(bot)


bot_app = FlaskApp(name='bot_app')

api = APIConverter(bot_app)
phrases = PhrasesData(bot_app)
phrases.set_phrases()
