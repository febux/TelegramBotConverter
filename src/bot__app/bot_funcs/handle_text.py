from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from src.bot__app.bot_funcs.help import handle_help
from src.bot__app.extensions.api_currency import APIConverter
from src.bot__app.extensions.phrases_data import PhrasesData
from src.configs.redis import redis_conn


async def handle_text(bot: Bot, message: Message, api: APIConverter, phrases: PhrasesData):
    if message.chat.type == 'private':
        if message.text == phrases.keyboard_button_3:  # List of available currencies
            await bot.send_message(message.chat.id, f"{phrases.available_currency} \n "
                                                    f"{api.get_available_list_currency()}")
            redis_conn.hdel(message.chat.id, 'base_currency', 'amount', 'quote_currency')
        elif message.text == phrases.keyboard_button_4:  # Help
            await handle_help(bot, message, api, phrases)
            redis_conn.hdel(message.chat.id, 'base_currency', 'amount', 'quote_currency')
        elif message.text == phrases.keyboard_button_2:  # Currency conversion
            markup = InlineKeyboardMarkup(row_width=3)

            for currency in api.currencies:  # перебираем ключи валют и создаём инлайн кнопки с их названиями
                markup.add(InlineKeyboardButton(
                    currency.currency_abbr,
                    callback_data=currency.currency_abbr + '_base'),
                )

            # отсылаем сообщение и включаем инлайн кнопки
            await bot.send_message(message.chat.id, phrases.quote_currency_question, reply_markup=markup)
            redis_conn.hdel(message.chat.id, 'base_currency', 'amount', 'quote_currency')
        elif message.text == phrases.keyboard_button_1:  # Currency exchange rate
            markup = InlineKeyboardMarkup(row_width=3)

            for currency in api.currencies:  # перебираем ключи валют и создаём инлайн кнопки с их названиями
                markup.add(InlineKeyboardButton(currency.currency_abbr, callback_data=currency.currency_abbr))

            # отсылаем сообщение и включаем инлайн кнопки
            await bot.send_message(message.chat.id, phrases.base_currency_question, reply_markup=markup)
            redis_conn.hdel(message.chat.id, 'base_currency', 'amount', 'quote_currency')
        else:
            if int(redis_conn.hget(message.chat.id, 'amount').decode('utf-8')) == -1:
                redis_conn.hset(message.chat.id, 'amount', message.text)  # устанавливаем сумму
                markup = InlineKeyboardMarkup(row_width=3)

                for currency in api.currencies:  # перебираем ключи и создаём кнопки
                    markup.add(InlineKeyboardButton(
                        currency.currency_abbr,
                        callback_data=currency.currency_abbr + '_exc'),
                    )  # добавляем кнопки

                await bot.send_message(message.chat.id, f"{phrases.currency_amount} {message.text}")
                await bot.send_message(message.chat.id, phrases.currency_name_question, reply_markup=markup)
            else:
                await bot.send_message(message.chat.id, phrases.wrong_text)
                redis_conn.hdel(message.chat.id, 'base_currency', 'amount', 'quote_currency')
