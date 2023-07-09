import os
import importlib

from src.utils.app_utils.initial import FlaskApp
from src.utils.db_utils.models_config import DbConfig
from src.configs.bot_db__config import db, migrate


host = os.environ['INTERNAL_API_RUN_HOST']
port = os.environ['INTERNAL_API_RUN_PORT']

# host = '0.0.0.0'
# port = 8090


internal_api_flask_app = FlaskApp(
    name='internal_api_flask_app',
    db_config=DbConfig(uri=os.environ['SQLALCHEMY_DATABASE_URI']),
)
internal_api_flask_app.connect_db_to_app(db, migrate)
route_files, ignored_route_files, mdl_list = internal_api_flask_app.load_routes()


for module in mdl_list:
    package = importlib.import_module(module)

    for name, value in package.__dict__.items():
        if not name.startswith("__"):
            globals()[name] = value


if __name__ == "__main__":
    internal_api_flask_app.register_test_route()
    internal_api_flask_app.run(host=host, port=int(port))
