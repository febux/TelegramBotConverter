import os
from typing import List, Type

from flask_admin.contrib.sqla import ModelView

from src.bot__db.app import db_flask_app

from src.bot__db.model_views import CurrencyView, LanguageView, PhraseView, TranslationView

host = os.environ['FLASK_RUN_HOST']
port = os.environ['FLASK_RUN_PORT']

VIEW_LIST: List[Type[ModelView]] = [CurrencyView, LanguageView, PhraseView, TranslationView]


if __name__ == "__main__":
    db_flask_app.load_models_to_admin_panel(VIEW_LIST)
    db_flask_app.app.run(host=host, port=int(port))
