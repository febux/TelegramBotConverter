from typing import Dict, Any, List
from uuid import UUID

from src.bot__db import Translation, Language, Phrase
# from src.bot__db.app import db_flask_app
from src.bot__db.models.base_model import BaseModel
from src.utils.db_utils.abs_repo import AbstractRepository
from src.utils.db_utils.db_app_context import db_app_context


class TranslationRepository(AbstractRepository):
    model = Translation

    @classmethod
    def add(cls):
        pass

    @classmethod
    def get(cls, identifier: UUID) -> BaseModel:
        pass

    @classmethod
    def get_all(cls) -> List[BaseModel]:
        pass

    @classmethod
    def update(cls, identifier: UUID) -> BaseModel:
        pass

    @classmethod
    def delete(cls, identifier: UUID) -> None:
        pass

    @classmethod
    @db_app_context
    def get_by_lang_phrase(cls, lang: str, phrase_key: str) -> Dict[str, Any]:
        language = Language.query.filter_by(language_abbr=lang).first()
        phrase = Phrase.query.filter_by(phrase_key=phrase_key).first()
        result = cls.model.query.filter_by(language_id=language.identifier, phrase_id=phrase.identifier).first()
        return result.to_dict()
