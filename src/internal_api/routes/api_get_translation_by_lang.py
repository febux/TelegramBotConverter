import logging

from flask import json
from markupsafe import escape

from src.bot__db.models.helpers import TranslationRepository
from src.internal_api.app import internal_api_flask_app


@internal_api_flask_app.route(["GET"], '/translations/<string:lang>/<string:phrase>')
def get_translation_by_lang(lang: str, phrase: str):
    try:
        result = TranslationRepository.get_by_lang_phrase(escape(lang), escape(phrase))
    except Exception as e:
        logging.exception(e)
        result = {}
    else:
        logging.info(result)
    return json.dumps(result)
