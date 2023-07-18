import logging

from aiogram import Bot
from aiogram.types import CallbackQuery

from src.bot__app.extensions.api_currency import APIConverter
from src.bot__app.extensions.phrases_data import PhrasesData
from src.configs.redis import redis_conn


async def callback_text(bot: Bot, callback: CallbackQuery, api: APIConverter, phrases: PhrasesData):
    # обрабатываем сообщения callback
    try:
        if callback.message:
            call_back = callback.data.split('_')
            len_callback = len(call_back)
            base_currency = call_back[0]
            flag = call_back[1] if len_callback > 1 else ''
            # обработка "Курс обмена валют"
            currencies = [cur.currency_abbr for cur in api.currencies]
            if len_callback == 1 and base_currency in currencies:
                # удаление инлайн кнопок и изменение сообщения
                await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            text=f"{phrases.related_1} {base_currency} ", reply_markup=None)

                for exchange_currency in currencies:
                    if exchange_currency == base_currency:
                        continue
                    await bot.send_message(
                        callback.message.chat.id,
                        f"1 {base_currency} = {api.get_rate(base_currency, exchange_currency)} {exchange_currency}",
                    )

            # обработка "Конверсия валют" валютное основание
            if len_callback == 2 and base_currency in currencies and flag == 'base':
                redis_conn.hset(callback.message.chat.id, mapping={
                    'base_currency': base_currency,
                    'amount': '-1',
                    'quote_currency': '',
                })

                await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            text=f"{phrases.your_choice} {base_currency}.", reply_markup=None)

                await bot.send_message(callback.message.chat.id, phrases.currency_amount_question)

            # обработка "Конверсия валют" валютная квота
            if len_callback == 2 and base_currency in currencies and flag == 'exc':
                redis_conn.hset(callback.message.chat.id, 'quote_currency', base_currency)
                await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            text=f"{phrases.your_choice} {base_currency}.", reply_markup=None)
                base_currency_user_conversion = redis_conn.hget(callback.message.chat.id, 'base_currency').decode('utf-8')
                amount_user_conversion = redis_conn.hget(callback.message.chat.id, 'amount').decode('utf-8')
                quote_currency_user_conversion = redis_conn.hget(callback.message.chat.id, 'quote_currency').decode('utf-8')
                conv_amount = api.get_rate(
                    base_currency_user_conversion,
                    quote_currency_user_conversion,
                    int(amount_user_conversion),
                )
                await bot.send_message(callback.message.chat.id, f" {amount_user_conversion}"
                                                                 f" {base_currency_user_conversion}"
                                                                 f" = {conv_amount} {quote_currency_user_conversion}")

                redis_conn.hdel(callback.message.chat.id, 'base_currency', 'amount', 'quote_currency')

            # show alert
            # bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
            #                           text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ")

    except Exception as e:
        logging.error(e)
