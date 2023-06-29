from aiogram.utils import executor

from extensions.pre_post_func import on_startup, on_shutdown
from src.bot__app.bot_funcs.start import handle_start
from src.bot__app.bot_funcs.help import handle_help
from src.bot__app.bot_funcs.handle_text import handle_text
from src.configs.self_logging import self_logging   # noqa

from aiogram.types import Message

from app import dp, api, bot


@dp.message_handler(commands=['start'])
async def start_processing(message: Message):
    await handle_start(bot=bot, message=message, api=api)


@dp.message_handler(commands=['help'])
async def help_processing(message: Message):
    await handle_help(bot=bot, message=message, api=api)


@dp.message_handler(content_types=['text'])
async def message_text_processing(message: Message):
    await handle_text(bot=bot, message=message, api=api)


@dp.callback_query_handler(lambda callback_query: True)
async def callback_inline(call):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup, on_shutdown=on_shutdown)
