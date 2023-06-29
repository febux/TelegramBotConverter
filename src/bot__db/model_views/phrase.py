from flask_admin.contrib.sqla import ModelView

from src.bot__db import Phrase
from src.bot__db.db import db


class PhraseView(ModelView):
    """
    Admin manager for Phrase
    """
    column_display_pk = True

    def __init__(self):
        super(PhraseView, self).__init__(Phrase, db.session, category='Phrase')
