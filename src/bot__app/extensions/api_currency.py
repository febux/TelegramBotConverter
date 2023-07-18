import requests
import lxml.html

from src.bot__app.model_response.currency import ApiCurrencyResponse
from src.configs.internal_api import internal_api

from src.utils.app_utils.initial import FlaskApp


def get_rate__freecurrencyrates(base: str, quote: str, amount: int = 1) -> str:
    req_curr = requests.get(f'https://freecurrencyrates.com/ru/'
                            f'convert-{base}-{quote}#{amount}').content
    req_curr_content = lxml.html.document_fromstring(req_curr)
    exchange_rate = req_curr_content.xpath('/html/body/main/div/div[2]/div[1]/div[1]'
                                           '/div[2]/div[2]/input/@value')
    exchange_rate = float(exchange_rate[0])
    result = float(amount) * exchange_rate
    result = format(float(result), '.2f')
    return result


# класс интерфейса приложения по конвертации валют
class APIConverter:
    def __init__(self, bot_app: FlaskApp):
        self._bot_app = bot_app
        with self._bot_app.app.app_context():
            self.currencies = internal_api.request_get(
                '/currencies',
                payload_type=ApiCurrencyResponse,
            )

    # статический метод конвертации валют, полученных с сайта
    # входные параметры берутся из вне
    @staticmethod
    def get_rate(base: str, quote: str, amount: int = 1):
        return get_rate__freecurrencyrates(base, quote, amount)

    # метод получения списка доступных валют
    def get_available_list_currency(self):
        with self._bot_app.app.app_context():
            self.currencies = internal_api.request_get(
                '/currencies',
                payload_type=ApiCurrencyResponse,
            )
        available_list_currency = ''
        for key in self.currencies:
            available_list_currency = '\n - '.join((available_list_currency, key.currency_name))
        return available_list_currency
