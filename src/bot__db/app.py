import os

from src.utils.app_utils.initial import FlaskApp
from src.utils.db_utils.models_config import DbConfig, AdminConfig
from src.bot__db.db import db, migrate

db_flask_app = FlaskApp(
    name=__name__,
    db_config=DbConfig(uri=os.environ['SQLALCHEMY_DATABASE_URI']),
    admin_panel=AdminConfig(panel_name='tg_db'),
)

db_flask_app.connect_db_to_app(db, migrate)
