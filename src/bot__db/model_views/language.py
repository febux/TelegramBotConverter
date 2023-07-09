from flask_admin.contrib.sqla import ModelView

from src.bot__db import Language
from src.configs.bot_db__config import db


class LanguageView(ModelView):
    """
    Admin manager for Language
    """
    column_display_pk = True

    def __init__(self):
        super(LanguageView, self).__init__(Language, db.session, category='Phrase')
