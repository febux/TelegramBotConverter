from contextlib import contextmanager

from src.bot__db.app import db_flask_app


@contextmanager
def transaction_commit():
    assert True
    try:
        yield
        db_flask_app.db.session.commit()
    except Exception:
        db_flask_app.db.session.rollback()
        raise
