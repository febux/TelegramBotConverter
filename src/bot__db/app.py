import os
from typing import List, Type

from flask_admin.contrib.sqla import ModelView

from src.bot__db.model_views import CurrencyView, LanguageView, PhraseView, TranslationView

from src.utils.app_utils.initial import FlaskApp
from src.utils.db_utils.models_config import DbConfig, AdminConfig
from src.configs.bot_db__config import db, migrate


host = os.environ['ADMIN_PANEL_RUN_HOST']
port = os.environ['ADMIN_PANEL_RUN_PORT']

# host = '0.0.0.0'
# port = 8080


db_flask_app = FlaskApp(
    name='db_flask_app',
    db_config=DbConfig(uri=os.environ['SQLALCHEMY_DATABASE_URI']),
    admin_panel=AdminConfig(panel_name='tg_db', admin_swatch='cosmo'),
)
db_flask_app.connect_db_to_app(db, migrate)

VIEW_LIST: List[Type[ModelView]] = [CurrencyView, LanguageView, PhraseView, TranslationView]


if __name__ == "__main__":
    db_flask_app.load_models_to_admin_panel(VIEW_LIST)
    db_flask_app.app.run(host=host, port=int(port))
