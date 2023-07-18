from src.bot__app.model_response.translation import ApiTranslationResponse
from src.configs.bot_app__config import LANG_SETTING

from src.configs.internal_api import internal_api

from src.utils.app_utils.initial import FlaskApp


class PhrasesData:
    def __init__(self, bot_app: FlaskApp):
        self._bot_app = bot_app
        self.help_text = ''
        self.welcome = ''
        self.start = ''
        self.keyboard_button_1 = ''
        self.keyboard_button_2 = ''
        self.keyboard_button_3 = ''
        self.keyboard_button_4 = ''
        self.quote_currency_question = ''
        self.base_currency_question = ''
        self.related_1 = ''
        self.your_choice = ''
        self.currency_amount = ''
        self.currency_amount_question = ''
        self.currency_name_question = ''
        self.wrong_text = ''
        self.available_currency = ''

    def set_phrases(self):
        with self._bot_app.app.app_context():
            self.help_text = internal_api.request_get(
                f'/translations/{LANG_SETTING}/help',
                payload_type=ApiTranslationResponse,
            ).translation_content

            self.welcome = internal_api.request_get(
                f'/translations/{LANG_SETTING}/welcome',
                payload_type=ApiTranslationResponse,
            ).translation_content
            self.start = internal_api.request_get(
                f'/translations/{LANG_SETTING}/start',
                payload_type=ApiTranslationResponse,
            ).translation_content
            self.wrong_text = internal_api.request_get(
                f'/translations/{LANG_SETTING}/wrong_text',
                payload_type=ApiTranslationResponse,
            ).translation_content

            self.keyboard_button_1 = internal_api.request_get(
                f'/translations/{LANG_SETTING}/keyboard_button_1',
                payload_type=ApiTranslationResponse,
            ).translation_content
            self.keyboard_button_2 = internal_api.request_get(
                f'/translations/{LANG_SETTING}/keyboard_button_2',
                payload_type=ApiTranslationResponse,
            ).translation_content
            self.keyboard_button_3 = internal_api.request_get(
                f'/translations/{LANG_SETTING}/keyboard_button_3',
                payload_type=ApiTranslationResponse,
            ).translation_content
            self.keyboard_button_4 = internal_api.request_get(
                f'/translations/{LANG_SETTING}/keyboard_button_4',
                payload_type=ApiTranslationResponse,
            ).translation_content
            self.available_currency = internal_api.request_get(
                f'/translations/{LANG_SETTING}/available_currency',
                payload_type=ApiTranslationResponse,
            ).translation_content
            self.base_currency_question = internal_api.request_get(
                f'/translations/{LANG_SETTING}/base_currency_question',
                payload_type=ApiTranslationResponse,
            ).translation_content
            self.quote_currency_question = internal_api.request_get(
                f'/translations/{LANG_SETTING}/quote_currency_question',
                payload_type=ApiTranslationResponse,
            ).translation_content
            self.related_1 = internal_api.request_get(
                f'/translations/{LANG_SETTING}/related_1',
                payload_type=ApiTranslationResponse,
            ).translation_content
            self.your_choice = internal_api.request_get(
                f'/translations/{LANG_SETTING}/your_choice',
                payload_type=ApiTranslationResponse,
            ).translation_content
            self.currency_amount = internal_api.request_get(
                f'/translations/{LANG_SETTING}/currency_amount',
                payload_type=ApiTranslationResponse,
            ).translation_content
            self.currency_amount_question = internal_api.request_get(
                f'/translations/{LANG_SETTING}/currency_amount_question',
                payload_type=ApiTranslationResponse,
            ).translation_content
            self.currency_name_question = internal_api.request_get(
                f'/translations/{LANG_SETTING}/currency_name_question',
                payload_type=ApiTranslationResponse,
            ).translation_content
