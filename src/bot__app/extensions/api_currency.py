import requests
import lxml.html
# import ast


# класс интерфейса приложения по конвертации валют
class API:
    def __init__(self, currencies=None):
        self.currencies = currencies

    # статический метод конвертации валют, полученных с сайта
    # входные параметры берутся из вне
    # @staticmethod
    # def get_rate(base, quote, amount=1):
    #     req_curr = requests.get(f'https://freecurrencyrates.com/ru/'
    #                             f'convert-{base}-{quote}#{amount}').content
    #     req_curr_content = lxml.html.document_fromstring(req_curr)
    #     exchange_rate = req_curr_content.xpath('/html/body/main/div/div[2]/div[1]/div[1]'
    #                                            '/div[2]/div[2]/input/@value')
    #     exchange_rate = float(exchange_rate[0])
    #     result = float(amount) * exchange_rate
    #     result = format(float(result), '.2f')
    #     return result

    # метод конвертации валют, полученных с сайта, записанные в класс
    # входные параметры берутся из объекта класса
    # @staticmethod
    # def get_rate_self(base, quote, amount):
    #     req_curr = requests.get(f'https://freecurrencyrates.com/ru/'
    #                             f'convert-{base}-{quote}#{amount}').content
    #     req_curr_content = lxml.html.document_fromstring(req_curr)
    #     exchange_rate = req_curr_content.xpath('/html/body/main/div/div[2]/div[1]/div[1]'
    #                                            '/div[2]/div[2]/input/@value')
    #
    #     result = format(float(amount) * float(exchange_rate[0]), '.2f')
    #     return result

    # метод получения списка доступных валют
    def get_available_list_currency(self):
        phrase = self.phrases_list.get('phrase_available_currency')
        available_list_currency = phrase  # выдаём список доступных валют
        for key in self.currencies.keys():  # перебираем в цикле ключи словаря с валютами
            available_list_currency = '\n - '.join((available_list_currency, key,))  # соединяем их в строке
        return available_list_currency

    # метод получения списка доступных валют
    @property
    def currency_list(self):
        return self.currencies

    # метод установки списка доступных валют
    # def set_list_currency(self, filename: str = 'currencies.yaml'):
    #     file = open(filename, 'r', encoding='UTF-8')  # открываем файл для чтения
    #     currencies = file.read()  # читаем весь файл с валютами
    #     self.currencies = ast.literal_eval(currencies)  # переводим полученный данные в словарь
    #     file.close()

    # метод установки списка доступных валют
    # def set_list_phrases(self, filename: str = 'phrases.yaml'):
    #     with open(filename, 'r') as file:
    #         file = open(filename, 'r', encoding='UTF-8')  # открываем файл для чтения
    #         phrases = yaml.safe_load(filename)
    #     self.phrases = ast.literal_eval(phrases)  # переводим полученный данные в словарь
    #     file.close()
