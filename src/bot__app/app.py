import os

from aiogram import Bot, Dispatcher

from extensions.api_currency import API

tg_token = os.environ['TG_TOKEN']
lang = os.environ['LANG_SETTING']

bot = Bot(token=tg_token)
dp = Dispatcher(bot)
api = API()
