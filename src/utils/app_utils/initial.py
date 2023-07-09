import logging
import os
from functools import wraps
from typing import Optional, List, Type, Any, Callable, TypeVar, cast

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from src.utils.api_utils.load_modules import load_modules_by_template
from src.utils.db_utils.models_config import DbConfig, AdminConfig


APPLICATION_ENV__LOCAL = 'local'


APPLICATION_ENV: str = os.environ.get('APPLICATION_ENV', APPLICATION_ENV__LOCAL)
APPLICATION_ENV_IS_LOCAL = APPLICATION_ENV == APPLICATION_ENV__LOCAL

APPLICATION_DIR: str = os.path.abspath(os.environ.get('APPLICATION_DIR', os.getcwd()))
APPLICATION_TMP: str = os.path.join(APPLICATION_DIR, '.tmp')

APPLICATION_UNDER_DOCKER = '/docker_app/' in os.getcwd()

APPLICATION_DEBUG = os.environ.get('APPLICATION_DEBUG', '0') == '1'


TFn = TypeVar("TFn", bound=Callable[..., Any])


class FlaskApp:
    def __init__(self, name: str, db_config: DbConfig = None, admin_panel: AdminConfig = None):
        self._app = Flask(
            import_name=name,
            static_url_path=None,
            static_folder=os.path.join(APPLICATION_DIR, 'static'),
            template_folder=os.path.join(APPLICATION_DIR, 'templates'),
        )
        self._fn_registry: List[Any] = []
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

    @staticmethod
    def load_routes():
        route_files, ignored_route_files, mdl_list = load_modules_by_template([
            os.path.join(APPLICATION_DIR, 'routes', 'api_*.py'),
            os.path.join(APPLICATION_DIR, 'routes', '**', 'api_*.py'),
            os.path.join(APPLICATION_DIR, 'views', 'view_*.py'),
            os.path.join(APPLICATION_DIR, 'views', '**', 'view_*.py'),
        ])

        return route_files, ignored_route_files, mdl_list

    def register_test_route(self):
        @self.route(['GET'], '/test')
        def test_page():
            return '<h1>Testing the Flask Application Factory Pattern</h1>'

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

    @property
    def fn_registry(self):
        return self._fn_registry

    def route(
            self,
            methods: List[str],
            path: str,
    ) -> Callable[[TFn], TFn]:
        def wrap(fn: TFn) -> TFn:
            assert self.app is not None, 'app must be initialized'
            assert fn.__module__, 'empty __module__ of function'

            logging.getLogger(fn.__module__)

            @wraps(fn)
            def wrapper(**kwargs: Any) -> Any:
                result = None
                self._fn_registry.append(fn)
                if result is None:
                    try:
                        result = self.app.ensure_sync(fn)(**kwargs)
                    except Exception as e:  # noqa: B902
                        result = e
                return result

            wrapper = self.app.route(path, methods=methods)(wrapper)

            return cast(TFn, wrapper)

        return wrap

    def run(
            self,
            host: Optional[str] = None,
            port: Optional[int] = None,
            debug: Optional[bool] = None,
            load_dotenv: bool = True,
            **options: Any,
    ) -> None:
        self.app.run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)
