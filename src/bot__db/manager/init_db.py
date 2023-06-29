from src.bot__db.app import db_flask_app
from src.utils.db_utils.db_app_context import db_app_context


@db_app_context
def init_db():
    db_flask_app.db.drop_all()
    db_flask_app.db.create_all()
