from uuid import UUID

from src.bot__db import Translation, Language, Phrase
from src.bot__db.models.base_model import BaseModel
from src.utils.db_utils.abs_repo import AbstractRepository
from src.utils.db_utils.db_app_context import db_app_context


class TranslationRepository(AbstractRepository):
    def __init__(self):
        self.model = Translation

    def add(self):
        raise NotImplementedError

    def get(self, identifier: UUID) -> BaseModel:
        raise NotImplementedError

    def update(self, identifier: UUID) -> BaseModel:
        raise NotImplementedError

    def delete(self, identifier: UUID) -> None:
        raise NotImplementedError

    @db_app_context
    def get_by_lang_phrase(self, lang: str, phrase_key: str) -> BaseModel:
        language = Language.query.filter_by(language_abbr=lang).first()
        phrase = Phrase.query.filter_by(phrase_key=phrase_key).first()
        return self.model.query.filter_by(language_id=language.identifier, phrase_id=phrase.identifier).first()


translation_db_repo = TranslationRepository()
