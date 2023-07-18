from src.utils.api_utils.internal_api import JsonApiPayload


class ApiCurrencyResponse(JsonApiPayload):
    currency_abbr: str
    currency_name: str
