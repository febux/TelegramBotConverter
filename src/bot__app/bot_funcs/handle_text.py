from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from src.bot__app.bot_funcs.help import handle_help
from src.bot__app.extensions.api_currency import API


async def handle_text(bot: Bot, message: Message, api: API):
    if message.chat.type == 'private':
        if message.text == api.phrases_list.get('keyboardButton3'):
            await bot.send_message(message.chat.id, api.get_available_list_currency())
        elif message.text == api.phrases_list.get('keyboardButton4'):
            await handle_help(bot, message, api)
        elif message.text == api.phrases_list.get('keyboardButton2'):
            markup = InlineKeyboardMarkup(row_width=3)
            buttons = {}
            index = 0

            for key in api.currency_list.keys():  # перебираем ключи валют и создаём инлайн кнопки с их названиями
                buttons[index] = InlineKeyboardButton(api.currency_list.get(key), callback_data=key + '_base')
                markup.add(buttons.get(index))
                index += 1

            # отсылаем сообщение и включаем инлайн кнопки
            await bot.send_message(message.chat.id, api.phrases_list.get('phrase_kB2'), reply_markup=markup)

        elif message.text == api.phrases_list.get('keyboardButton1'):

            markup = InlineKeyboardMarkup(row_width=3)
            buttons = {}
            index = 0

            for key in api.currency_list.keys():  # перебираем ключи валют и создаём инлайн кнопки с их названиями
                buttons[index] = InlineKeyboardButton(api.currency_list.get(key), callback_data=key)
                markup.add(buttons.get(index))
                index += 1

            # отсылаем сообщение и включаем инлайн кнопки
            await bot.send_message(message.chat.id, api.phrases_list.get('phrase_kB1'), reply_markup=markup)
        else:
            await bot.send_message(message.chat.id, api.phrases_list.get('phrase_wrong_text'))
