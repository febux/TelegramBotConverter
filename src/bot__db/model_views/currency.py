from flask_admin.contrib.sqla import ModelView

from src.bot__db import Currency
from src.configs.bot_db__config import db


class CurrencyView(ModelView):
    """
    Admin manager for Currency
    """
    column_display_pk = True

    def __init__(self):
        super(CurrencyView, self).__init__(Currency, db.session)
