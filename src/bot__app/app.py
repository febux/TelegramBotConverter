import os

from aiogram import Bot, Dispatcher

from extensions.api_currency import API
from src.utils.app_utils.initial import FlaskApp

tg_token = os.environ['TG_TOKEN']
lang = os.environ['LANG_SETTING']

bot = Bot(token=tg_token)
dp = Dispatcher(bot)
api = API()


bot_app = FlaskApp(name='bot_app')
