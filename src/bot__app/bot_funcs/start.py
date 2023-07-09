from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from src.bot__app.app import bot_app
from src.bot__app.extensions.api_currency import API
from src.bot__app.model_response.translation import ApiTranslationResponse
from src.configs.bot_app__config import LANG_SETTING
from src.configs.internal_api import internal_api


async def handle_start(bot: Bot, message: Message, api: API):
    with bot_app.app.app_context():
        welcome = internal_api.request_get(f'/translations/{LANG_SETTING}/welcome', payload_type=ApiTranslationResponse)
        start = internal_api.request_get(f'/translations/{LANG_SETTING}/start', payload_type=ApiTranslationResponse)
        keyboard_button_1 = internal_api.request_get(
            f'/translations/{LANG_SETTING}/keyboard_button_1',
            payload_type=ApiTranslationResponse,
        )
        keyboard_button_2 = internal_api.request_get(
            f'/translations/{LANG_SETTING}/keyboard_button_2',
            payload_type=ApiTranslationResponse,
        )
        keyboard_button_3 = internal_api.request_get(
            f'/translations/{LANG_SETTING}/keyboard_button_3',
            payload_type=ApiTranslationResponse,
        )
        keyboard_button_4 = internal_api.request_get(
            f'/translations/{LANG_SETTING}/keyboard_button_4',
            payload_type=ApiTranslationResponse,
        )

    # клавиатура бота
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # добавляем клавиатуру
    markup.add(
        KeyboardButton(keyboard_button_1.translation_content),
        KeyboardButton(keyboard_button_2.translation_content),
        KeyboardButton(keyboard_button_3.translation_content),
        KeyboardButton(keyboard_button_4.translation_content),
    )

    # отправляем сообщение и включаем клавиатуру
    await bot.send_message(message.chat.id, f"{welcome.translation_content}, {message.from_user.first_name}!")
    await bot.send_message(message.chat.id, start.translation_content, parse_mode='html', reply_markup=markup)
