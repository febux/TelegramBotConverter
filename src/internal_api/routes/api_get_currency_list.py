import logging

from flask import json

from src.bot__db.models.helpers import CurrencyRepository
from src.internal_api.app import internal_api_flask_app


@internal_api_flask_app.route(["GET"], '/currencies')
def get_currency_list():
    try:
        result = CurrencyRepository.get_all()
    except TypeError as e:
        logging.exception(e)
        result = {}
    except Exception as e:
        logging.exception(e)
        result = {}
    else:
        logging.info(result)
    return json.dumps(result)
