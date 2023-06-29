from functools import wraps
from typing import TypeVar, Any, Callable, cast

from src.bot__db.app import db_flask_app

TFn = TypeVar("TFn", bound=Callable[..., Any])


def db_app_context(func: TFn) -> TFn:
    @wraps(func)
    def new_func(*args: Any, **kwargs: Any) -> Any:
        with db_flask_app.app.app_context():
            return func(*args, **kwargs)
    return cast(TFn, new_func)
