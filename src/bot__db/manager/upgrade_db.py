from typing import List, Any
from uuid import UUID

from src.bot__db import Language, Currency, Phrase, Translation
from src.bot__db.app import db_flask_app
from src.utils.db_utils.db_app_context import db_app_context
from src.utils.db_utils.transaction_commit import transaction_commit


@db_app_context
def upgrade_db():
    db_flask_app.db.drop_all()
    db_flask_app.db.create_all()

    currencies: List[Any] = [
        Currency(currency_abbr='USD', currency_name='dollar'),
        Currency(currency_abbr='EUR', currency_name='euro'),
        Currency(currency_abbr='GBP', currency_name='pound'),
        Currency(currency_abbr='AED', currency_name='dirham'),
        Currency(currency_abbr='RUB', currency_name='ruble'),
        Currency(currency_abbr='BYN', currency_name='belarussian ruble'),
    ]

    eng = Language(identifier=UUID('9903fe63-692f-4233-a6ec-2156c91df16f'), language_abbr='ENG', language_name='English')
    rus = Language(identifier=UUID('a9761244-d17c-4f55-b0eb-cf7c2b0719a7'), language_abbr='RUS', language_name='Русский')

    languages: List[Any] = [
        eng,
        rus,
    ]

    help_phrase = Phrase(identifier=UUID('570ea584-dd4b-4828-8788-37a838e42a78'), phrase_key='help')
    welcome = Phrase(identifier=UUID('087af04d-3a90-44a8-9474-c8970298dec4'), phrase_key='welcome')
    start = Phrase(identifier=UUID('fa299177-2d9d-44ef-acb1-c303cfb403d0'), phrase_key='start')
    keyboard_button1 = Phrase(identifier=UUID('371ecdee-fc05-417d-8697-b2f485509715'), phrase_key='keyboard_button1')
    keyboard_button2 = Phrase(identifier=UUID('18c460ff-c773-4367-957a-30ddc02f606b'), phrase_key='keyboard_button2')
    keyboard_button3 = Phrase(identifier=UUID('fa9714d9-5666-4871-bac2-4ee3bbd21e5c'), phrase_key='keyboard_button3')
    keyboard_button4 = Phrase(identifier=UUID('0d08a694-f881-4fee-af47-a7fb5a632f46'), phrase_key='keyboard_button4')
    quote_currency_question = Phrase(identifier=UUID('a359a3f0-bf79-4798-8d6c-f18d2e53324a'), phrase_key='quote_currency_question')
    base_currency_question = Phrase(identifier=UUID('cd7a38db-b943-4940-a087-78162cf50c8c'), phrase_key='base_currency_question')
    related_1 = Phrase(identifier=UUID('f5ea39ca-34d3-459a-ad62-de29686e1611'), phrase_key='related_1')
    your_choice = Phrase(identifier=UUID('8d747a0f-18d4-4db1-88af-21f0b275a94d'), phrase_key='your_choice')
    currency_amount = Phrase(identifier=UUID('5209ab44-20c7-43e6-8b0f-52a663cb97fc'), phrase_key='currency_amount')
    currency_name_question = Phrase(identifier=UUID('f0c4b382-42fb-45d1-b4a5-b7843009a9be'), phrase_key='currency_name_question')
    wrong_text = Phrase(identifier=UUID('dfa711b4-655e-4e57-9253-9a5bc29151b3'), phrase_key='wrong_text')
    available_currency = Phrase(identifier=UUID('493f5b0c-14ec-467f-a2e0-71df27b6dff0'), phrase_key='available_currency')

    phrases: List[Any] = [
        help_phrase,
        welcome,
        start,
        keyboard_button1,
        keyboard_button2,
        keyboard_button3,
        keyboard_button4,
        quote_currency_question,
        base_currency_question,
        related_1,
        your_choice,
        currency_amount,
        currency_name_question,
        wrong_text,
        available_currency,
    ]

    with transaction_commit():
        db_flask_app.db.session.bulk_save_objects(currencies)
        db_flask_app.db.session.bulk_save_objects(languages)
        db_flask_app.db.session.bulk_save_objects(phrases)

    translations: List[Any] = [
        Translation(
            phrase_id=help_phrase.identifier,
            language_id=eng.identifier,
            content="To get the current exchange rate, click the \"Currency exchange rate\", "
                    "then select the currency you want to know the rate against. \n\n "
                    "To go to the currency converter, click the \"Currency conversion\", "
                    "then select the currency you want to sell, "
                    "then enter the currency amount, you want to sell, "
                    "then select the currency you want to buy and you will know "
                    "the amount of currency you want to purchase.\n\n "
                    "For getting a list of available currencies, "
                    "click the \"List of available currencies\" button.\n\n "
                    "For getting help with working with me, click the \"Help\" button.\n\n",
        ),
        Translation(
            phrase_id=help_phrase.identifier,
            language_id=rus.identifier,
            content="Для получения актуального курса обмена нажмите кнопку \""
                    "Курс обмена валют\", затем выберите валюту, относительно "
                    "которой хотите узнать курс.\n\nДля перехода в конвертер валют "
                    "нажмите кнопку \"Конверсия валют\", затем выберите выберите валюту, "
                    "которую хотите продать, потом введите сумму валюты, "
                    "которую хотите продать, затем выберите валюту, "
                    "которую хотите купить и вы узнаете сумму валюты, "
                    "которую вы хотите приобрести.\n\n"
                    "Для получения списка доступных валют нажмите кнопку "
                    "\"Список доступных валют\".\n\nДля получения помощи по "
                    "работе со мной нажмите кнопку \"Помощь\".\n\n",
        ),
    ]

    with transaction_commit():
        db_flask_app.db.session.bulk_save_objects(translations)
