from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from src.bot__app.extensions.api_currency import API


async def handle_start(bot: Bot, message: Message, api: API):
    # клавиатура бота
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = KeyboardButton(api.phrases_list.get('keyboardButton1'))
    button_2 = KeyboardButton(api.phrases_list.get('keyboardButton2'))
    button_3 = KeyboardButton(api.phrases_list.get('keyboardButton3'))
    button_4 = KeyboardButton(api.phrases_list.get('keyboardButton4'))

    # добавляем клавиатуру
    markup.add(button_1, button_2, button_3, button_4)

    # отправляем сообщение и включаем клавиатуру
    await bot.send_message(message.chat.id, f"Welcome {message.from_user}!")
    await bot.send_message(message.chat.id, api.phrases_list.get('start'), parse_mode='html',
                           reply_markup=markup)
