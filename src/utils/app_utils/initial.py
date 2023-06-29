import os
from typing import Optional, List, Type

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src.utils.db_utils.models_config import DbConfig, AdminConfig


APPLICATION_ENV__LOCAL = 'local'


APPLICATION_ENV: str = os.environ.get('APPLICATION_ENV', APPLICATION_ENV__LOCAL)
APPLICATION_ENV_IS_LOCAL = APPLICATION_ENV == APPLICATION_ENV__LOCAL

APPLICATION_DIR: str = os.path.abspath(os.environ.get('APPLICATION_DIR', os.getcwd()))
APPLICATION_TMP: str = os.path.join(APPLICATION_DIR, '.tmp')

APPLICATION_UNDER_DOCKER = '/docker_app/' in os.getcwd()

APPLICATION_DEBUG = os.environ.get('APPLICATION_DEBUG', '0') == '1'


class FlaskApp:
    def __init__(self, name: str, db_config: DbConfig = None, admin_panel: AdminConfig = None):
        self._app = Flask(name)
        self._app.config['DEBUG'] = APPLICATION_ENV_IS_LOCAL and APPLICATION_DEBUG
        self._app.config['EXPLAIN_TEMPLATE_LOADING'] = False
        self._app.config['ENV'] = 'development' if APPLICATION_DEBUG else 'production'
        self._app.config['SECRET_KEY'] = 'some-long-long-secret-only-for-wtforms-string-be-brave-if-you-use-it-on-prod'
        self._app.config['TEMPLATES_AUTO_RELOAD'] = APPLICATION_DEBUG and APPLICATION_ENV_IS_LOCAL
        self._app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
        self._app.config['JSON_SORT_KEYS'] = False
        self._app.config['PREFERRED_URL_SCHEME'] = 'http'
        self._app.config['APPLICATION_ROOT'] = APPLICATION_DIR

        if db_config:
            self._app.config['SQLALCHEMY_DATABASE_URI'] = db_config.uri
            self._app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = db_config.track_mod
            self._app.config['SQLALCHEMY_POOL_RECYCLE'] = db_config.pool_recycle
            self._app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
                "pool_pre_ping": db_config.pool_pre_ping,
            }
            self._app.config['SQLALCHEMY_RECORD_QUERIES'] = db_config.record_queries

            self._db = SQLAlchemy()
            self._migrate = Migrate()

        if admin_panel:
            self._app.config['FLASK_ADMIN_SWATCH'] = admin_panel.admin_swatch
            self._admin = Admin(self._app, name=admin_panel.panel_name, template_mode='bootstrap3')

    def connect_db_to_app(self, db: Optional[SQLAlchemy] = None, migrate: Optional[Migrate] = None):
        self.db = db if db else self.db
        self.db.init_app(self.app)
        self.migrate = migrate if migrate else self.migrate
        self.migrate.init_app(self.app, self.db)

    def load_models_to_admin_panel(self, views: List[Type[ModelView]]):
        for view in views:
            self._admin.add_view(view())    # type: ignore

    @property
    def app(self):
        return self._app

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, instance: SQLAlchemy):
        self._db = instance

    @property
    def migrate(self):
        return self._migrate

    @migrate.setter
    def migrate(self, instance: Migrate):
        self._migrate = instance

    @property
    def admin(self):
        return self._admin
