from flask_admin.contrib.sqla import ModelView, fields
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from wtforms import SelectField

from src.bot__db import Translation, Phrase, Language
from src.bot__db.db import db


class TranslationView(ModelView):
    """
    Admin manager for Translation
    """
    column_display_pk = True
    column_list = ['identifier', 'phrase', 'language', 'content', 'created_at', 'updated_at']
    form_columns = column_list
    # form_overrides = {
    #     'phrase': SelectField,
    #     'language': SelectField,
    # }
    # form_choices = {
    #     'phrase': [
    #
    #     ],
    #     'language': [
    #
    #     ],
    # }

    form_args = {
        'phrase': {
            'query_factory': lambda: db.session.query(Phrase)
        },
        'language': {
            'query_factory': lambda: db.session.query(Language)
        }
    }

    def __init__(self):
        super(TranslationView, self).__init__(Translation, db.session, category='Phrase')
